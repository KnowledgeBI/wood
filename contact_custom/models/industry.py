# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartnerIndustry(models.Model):
    _inherit = "res.partner.industry"
    fiscal_position_id = fields.Many2one(comodel_name="account.fiscal.position", string="Fiscal Position",
                                         required=False, )
