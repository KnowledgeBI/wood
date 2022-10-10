""" Initialize Sale Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'sale.order'

    route_id = fields.Many2one(
        'sale.route'
    )
    route_line_id = fields.Many2one(
        'route.line'
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        related='route_line_id.vehicle_id'
    )
    driver_id = fields.Many2one(
        related='route_line_id.driver_id'
    )
    responsible_id = fields.Many2one(
        'res.users',
        readonly=1,
        string='Responsible',
        related='route_line_id.create_uid'
    )
    state_id = fields.Many2one(
        'res.country.state',
        related='route_line_id.state_id'
    )
    city = fields.Char(
        related='route_line_id.city'
    )