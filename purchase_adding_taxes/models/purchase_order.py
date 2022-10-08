# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    tax_ids = fields.Many2many(comodel_name="account.tax", string="Taxes", )

    def action_set_taxes(self):
        self.order_line.write({
            'taxes_id': self.tax_ids.ids
        })
