# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", copy=False,
                                          help="Link this project to an analytic account if you need financial management on projects. "
                                               "It enables you to connect projects with budgets, planning, cost and revenue analysis, timesheets on projects, etc.")

    @api.model
    def create(self, vals_list):
        """ Override create """
        # vals_list ={'field': value}  -> dectionary contains only new filled fields
        res = super(AccountPayment, self).create(vals_list)
        if res.move_id.line_ids:
            for line in res.move_id.line_ids:
                line.update({
                    'analytic_account_id': res.analytic_account_id.id,
                    'analytic_tag_ids': [(6, 0, res.analytic_tag_ids.ids)],
                            })
        return res


    @api.onchange('analytic_account_id', 'analytic_tag_ids')
    @api.constrains('analytic_account_id', 'analytic_tag_ids')
    def _onchange_analytic_account_id(self):
        """ analytic_account_id """
        for rec in self:
            if rec.move_id.line_ids:
                for line in rec.move_id.line_ids:
                    line.update({
                        'analytic_account_id': rec.analytic_account_id.id,
                        'analytic_tag_ids': [(6, 0, rec.analytic_tag_ids.ids)],
                    })