""" Initialize Fleet Vehicle """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class FleetVehicle(models.Model):
    """
        Inherit Fleet Vehicle:
         -
    """
    _inherit = 'fleet.vehicle'

    warehouse_id = fields.Many2one(
        'stock.warehouse'
    )