""" Initialize Pos Config """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class PosConfig(models.Model):
    """
        Inherit Pos Config:
         -
    """
    _inherit = 'pos.config'

    show_tax_info = fields.Boolean()