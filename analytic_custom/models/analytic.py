# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class Analytic(models.Model):
    _inherit = 'account.analytic.account'

    type = fields.Selection(string="Type", selection=[
        ('project', 'Project'),
        ('internal', 'Internal'),
        ('bank_deposit', 'Bank Deposit'),
        ('letter_of_guarantee', 'Letter Of Guarantee'),
        ('letter_of_credit', 'Letter Of Credit'),
    ], required=False)
    old_ref = fields.Char(string="Old Ref", required=False, )
    contract_date = fields.Date(string="Contract Date", required=False, )
    start_date = fields.Date(string="Expected Start Date", required=False, )
    end_date = fields.Date(string="Expected End Date", required=False, )
    analytic_status_id = fields.Many2one(comodel_name="analytic.status", string="Status", required=False, )
    analytic_priority_id = fields.Many2one(comodel_name="analytic.priority", string="Priority", required=False, )
    contract_amount = fields.Monetary(string="Contract Amount", required=False, )
    estimated_cost = fields.Monetary(string="Estimated Cost", required=False, )
    actual_cost = fields.Monetary(string="Actual Cost", compute='_compute_actual_cost')

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date > rec.end_date:
                raise exceptions.ValidationError('Expected End Date must be greater than Expected Start Date !')

    @api.model
    def create(self, vals):
        rec = super(Analytic, self).create(vals)
        if rec.group_id:
            if rec.group_id.sequence_id:
                sequence = ''
                if rec.group_id.parent_id and rec.group_id.parent_id.prefix:
                    sequence += "{}-".format(rec.group_id.parent_id.prefix)
                if rec.group_id.prefix:
                    sequence += "{}-".format(rec.group_id.prefix)
                sequence += "{}".format(rec.group_id.sequence_id.next_by_id())
                rec.code = sequence
        return rec

    def _compute_actual_cost(self):
        for rec in self:
            balance = 0.0
            if rec.id:
                items = self.env['account.move.line'].search([
                    ('account_id.is_costing', '=', True),
                    ('analytic_account_id', '=', rec.id),
                ])
                debit = sum(items.mapped('debit'))
                credit = sum(items.mapped('credit'))
                balance = debit - credit
            rec.actual_cost = balance


class Status(models.Model):
    _name = 'analytic.status'
    _rec_name = 'name'
    _description = 'Analytic Status'

    name = fields.Char(required=True)


class Priority(models.Model):
    _name = 'analytic.priority'
    _rec_name = 'name'
    _description = 'Analytic priority'

    name = fields.Char(required=True)
