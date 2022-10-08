# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('warehouse_id', 'partner_id')
    def _onchange_warehouse_id(self):
        for rec in self:
            if rec.env.user.stock_location_ids:
                warehouses_ids = self.env['stock.warehouse'].search([('lot_stock_id', 'child_of', rec.env.user.stock_location_ids.ids)])
                return {'domain': {'warehouse_id': [('id', 'in', warehouses_ids.ids)]}}

    @api.model
    def _default_warehouse_id(self):
        res = super(SaleOrder, self)._default_warehouse_id()
        if self.env.user.sale_warehouse_id:
            return self.env.user.sale_warehouse_id.id
        else:
            return False

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default=_default_warehouse_id)
