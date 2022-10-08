# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def write(self, vals):
        if any(x.custody_settlement for x in self.mapped('move_id')):
            return super(AccountMoveLine, self.with_context(escape_test = True)).write(vals)
        else:
            return super(AccountMoveLine, self).write(vals)

    attachment_file = fields.Binary('Attachment')
    attachment_name = fields.Char('Attachment')

class AccountMove(models.Model):
    _inherit = 'account.move'


    def is_purchase_document(self, include_receipts=False):
        res = super(AccountMove, self).is_purchase_document(include_receipts)
        if self.env.context.get('escape_test'):
            return False
        return res

    employee_contacts = fields.Many2many('res.partner',compute='get_contacts')

    @api.depends('custody_settlement')
    def get_contacts(self):
        employees = self.env['hr.employee'].sudo().search([])
        employee_ids = employees.mapped('user_id').mapped('partner_id').ids
        for rec in self:
            rec.employee_contacts = employee_ids

    custody_settlement = fields.Boolean()
    partner_balance = fields.Monetary(string='Balance',compute='_compute_partner_balance',store=True, copy=False)
    estimated_balance = fields.Monetary(string='Estimated Balance',compute='compute_estimated_balance',store=True )
    approval_levels = fields.Selection(string="Approvals", selection=[
        ('none', 'None'),('waiting', 'Waiting Approve'), ('approved', 'Approved'), ], required='False',default='none' )
    analytic_tags_ids = fields.Many2many(comodel_name="account.analytic.tag",
                                         relation="rel_analytic_tags", column1="analytic_tag", column2="move_id",
                                         string="Analytic Tags")

    @api.onchange('analytic_tags_ids', 'invoice_line_ids')
    def set_analytic_tags(self):
        for rec in self:
            if rec.analytic_tags_ids:
                for line in rec.invoice_line_ids:
                    line.analytic_tag_ids = rec.analytic_tags_ids

    # @api.onchange('team_id')
    # def get_sector_journals(self):
    #     # super(AccountMove, self).get_sector_journals()
    #     for rec in self:
    #         if rec.team_id:
    #             if rec.move_type == 'in_invoice' and rec.custody_settlement:
    #                 rec.journal_id = rec.team_id.custody_journal_id.id or False

    @api.onchange('partner_id')
    @api.constrains('partner_id')
    def _check_valid_partner(self):
        for rec in self:
            if rec.custody_settlement and rec.partner_id and rec.partner_id != self.env.user.partner_id and self.env.user.has_group(
                    'custody_settlement.group_custody_user') and not self.env.user.has_group(
                'custody_settlement.group_custody_manager'):
                raise exceptions.ValidationError("You Can't create for another employee!")


    # @api.onchange('write_date')
    # @api.constrains('partner_id')
    def _compute_partner_balance(self):
        for rec in self:
            rec.partner_balance = abs(rec.partner_id.credit) - abs(rec.partner_id.debit)

    @api.depends('amount_total','partner_balance')
    def compute_estimated_balance(self):
        for rec in self:
            rec.estimated_balance = rec.partner_balance - rec.amount_total

    def request_approve(self):
        self.approval_levels='waiting'

    def action_post(self):
        res = super(AccountMove, self).action_post()
        self.approval_levels='approved'
        return res

    @api.onchange('custody_settlement')
    def onchange_get_default_partner(self):
        for rec in self:
            if rec.custody_settlement:
                if self.env.user.partner_id.id in rec.employee_contacts.ids:
                    rec.partner_id = self.env.user.partner_id.id

    @api.model
    def _get_tax_grouping_key_from_base_line(self, base_line, tax_vals):
        res = super(AccountMove, self)._get_tax_grouping_key_from_base_line(base_line, tax_vals)
        if base_line.move_id.custody_settlement:
            res.update({'partner_id': base_line.partner_id.id})
        return res

    @api.onchange('invoice_line_ids')
    def onchange_settelment(self):
        for invoice in self.filtered(lambda x: x.custody_settlement):
            lines = invoice.invoice_line_ids
            invoice.invoice_line_ids = invoice.line_ids = False
            invoice.invoice_line_ids = lines
            invoice.invoice_line_ids._onchange_mark_recompute_taxes()
            invoice._onchange_invoice_line_ids()
