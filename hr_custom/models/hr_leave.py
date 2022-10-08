""" Initialize Hr Leave """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrLeave(models.Model):
    """
        Inherit Hr Leave:
         - 
    """
    _inherit = 'hr.leave'

    barcode = fields.Char(
        related='employee_id.barcode',
        store=1
    )