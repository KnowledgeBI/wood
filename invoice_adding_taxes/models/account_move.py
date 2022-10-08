# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    tax_ids = fields.Many2many(comodel_name="account.tax", string="Taxes", )

    def action_set_taxes(self):
        for line in self.invoice_line_ids:
            line.tax_ids = self.tax_ids.ids
            line._onchange_mark_recompute_taxes()
        self.with_context(check_move_validity=False)._onchange_recompute_dynamic_lines()
