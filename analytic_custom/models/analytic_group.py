# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class AnalyticGroup(models.Model):
    _inherit = 'account.analytic.group'

    prefix = fields.Char(string="Prefix", required=False, )
    is_sector = fields.Boolean(string="Is Sector ?", )
    team_id = fields.Many2one(comodel_name="crm.team", string="Sales Team", required=False, )
    sequence_id = fields.Many2one(comodel_name="ir.sequence", string="Sequence", required=False, )

    @api.model
    def create(self, vals):
        rec = super(AnalyticGroup, self).create(vals)
        if not rec.sequence_id:
            sequence = self.env['ir.sequence'].sudo().create({
                'name': rec.name,
                'code': rec.prefix,
                'padding': 5,
                'company_id': rec.company_id.id
            })
            rec.write({
                'sequence_id': sequence.id
            })
        return rec
