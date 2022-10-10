""" Initialize Sale Routes """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleRoute(models.Model):
    """
        Initialize Sale Route:
         -
    """
    _name = 'sale.route'
    _description = 'Sale Route'
    
    name = fields.Char()
    date_from = fields.Date()
    date_to = fields.Date()

    # create_uid = fields.Many2one(
    #     'res.users',
    #     string='Responsible'
    # )
    route_line_ids = fields.One2many(
        'route.line',
        'sale_route_id'
    )

    state = fields.Selection(
        [('draft', 'Draft'),
         ('validate', 'Validated'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status'
    )

    @api.model
    def create(self, vals_list):
        """
            Override create method
             - sequence name 
        """
        res = super(SaleRoute, self).create(vals_list)
        res.name = self.env['ir.sequence'].next_by_code('SR') or _('New')
        return res
    
    def action_confirm(self):
        """ Action Confirm """
        for rec in self:
            rec.state = 'validate'

    def action_cancel(self):
        """ Action Confirm """
        for rec in self:
            rec.state = 'cancel'


class RouteLine(models.Model):
    """
        Initialize Route Line:
         -
    """
    _name = 'route.line'
    _description = 'Route Line'

    sale_route_id = fields.Many2one(
        'sale.route'
    )
    date = fields.Date()
    vehicle_id = fields.Many2one(
        'fleet.vehicle'
    )
    driver_id = fields.Many2one(
        'hr.employee',
        default=lambda self:self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1),
    )
    quotation_created = fields.Boolean(
        copy=False
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Customer'
    )
    state_id = fields.Many2one(
        'res.country.state', 
    )
    city = fields.Char()
    
    @api.constrains('date')
    def _check_date(self):
        """ Validate date """
        for rec in self:
            if rec.sale_route_id.date_from and rec.sale_route_id.date_to:
                if rec.date < rec.sale_route_id.date_from or rec.date > rec.sale_route_id.date_to:
                    raise ValidationError('Date must be in the range !')

    def create_quotation(self):
        """ Create Quotation """
        order = self.env['sale.order'].sudo().create({
            'date_order': self.date,
            'partner_id': self.partner_id.id,
            'route_id': self.sale_route_id.id,
            'route_line_id': self.id,
            'responsible_id': self.create_uid.id,
        })
        if self.vehicle_id.warehouse_id:
            order.update({
                'warehouse_id': self.vehicle_id.warehouse_id.id
            })
        self.quotation_created = True

