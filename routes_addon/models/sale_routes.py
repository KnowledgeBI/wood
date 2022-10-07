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
    date = fields.Date()
    vehicle_id = fields.Many2one(
        'fleet.vehicle'
    )
    driver_id = fields.Many2one(
        'hr.employee',
        default=lambda self:self.env['hr.employee'].search(
        [('user_id', '=', self.env.uid)], limit=1),
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('validate', 'Validated'),
         ('cancel', 'Cancel')],
        default='draft',
        string='Status'
    )
    # create_uid = fields.Many2one(
    #     'res.users',
    #     string='Responsible'
    # )
    route_line_ids = fields.One2many(
        'route.line',
        'sale_route_id'
    )
    # quotation_created = fields.Boolean()
    partner_id = fields.Many2one(
        'res.partner',
        'Customer'
    )

    @api.constrains('date')
    def _check_date(self):
        """ Validate date """
        for rec in self:
            if rec.date_from and rec.date_to:
                if rec.date < rec.date_from or rec.date > rec.date_to:
                    raise ValidationError('Date must be in the range !')

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

    def create_quotation(self):
        """ Create Quotation """
        order = self.env['sale.order'].sudo().create({
            'date_order': self.date,
            'partner_id': self.partner_id.id,
            'route_id': self.id,
            'responsible_id': self.create_uid.id,
        })
        if self.route_line_ids:
            for line in self.route_line_ids:
                order = self.env['sale.order.line'].sudo().create({
                    'order_id': order.id,
                    'product_id': line.product_id.id,
                    'price_unit': line.price_unit,
                    'product_uom_qty': line.qty,
                })


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
    product_id = fields.Many2one(
        'product.product'
    )
    qty = fields.Float()
    price_unit = fields.Float()
