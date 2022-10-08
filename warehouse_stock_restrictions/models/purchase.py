from odoo import fields, models, api
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase

READONLY_STATES = {
    'purchase': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _get_picking_type(self, company_id):
        picking_type_id = 0
        for line in self.env.user.default_picking_type_ids:
            if line.code == 'incoming':
                picking_type_id = line.id
        return picking_type_id 

    @api.model
    def _default_picking_type(self):
        picking_type_id = 0
        for line in self.env.user.default_picking_type_ids:
            if line.code == 'incoming':
                picking_type_id = line.id
        return picking_type_id if picking_type_id > 0 else \
            self._get_picking_type(self.env.context.get('company_id') or self.env.company.id)

    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To', states=Purchase.READONLY_STATES,
                                      required=True, default=_default_picking_type,
                                      domain="['|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]",
                                      help="This will determine operation type of incoming shipment")
