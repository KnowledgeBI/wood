# -*- coding: utf-8 -*-

from odoo import api, models, fields, _

class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_customer_info = fields.Boolean('Customer Info on Receipt')
