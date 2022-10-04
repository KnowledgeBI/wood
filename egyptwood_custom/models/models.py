# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLeadProduct(models.Model):
    _inherit = 'crm.lead'

    crm_products_ids = fields.One2many(comodel_name="crm.lead.products", inverse_name="crm_id", string="",
                                       required=False, )


class CrmLeadProducts(models.Model):
    _name = 'crm.lead.products'
    _rec_name = 'product_id'

    product_id = fields.Many2one(comodel_name="product.product", string="", required=False, )
    product_code = fields.Char(string="Code", related='product_id.default_code', store=True)
    crm_id = fields.Many2one(comodel_name="crm.lead", string="", required=False, )


class PurchaseOrderFor(models.Model):
    _inherit = 'purchase.order'

    for_in = fields.Boolean(string="Foreign", )


class ForinPurchase(models.Model):
    _name = 'forin.purchase'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'name'

    def _default_picking_type_id(self):
        picking_obj = self.env['stock.picking.type'].search([('is_transients', '=', True)], limit=1)
        return picking_obj.id

    def _default_sender_type_id(self):
        picking_obj = self.env['stock.picking.type'].search([('is_senders', '=', True)], limit=1)
        return picking_obj.id

    name = fields.Char(readonly=True, copy=False, default='New')
    state = fields.Selection(string="",
                             selection=[('production', 'Production'), ('atport', 'at Port'), ('onway', 'On Way'),
                                        ('egyport', 'Egypt Port'),
                                        ('delivered', 'Delivered'), ], default='production', tracking=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Vendor", required=True, )
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id.id)
    date_planned = fields.Datetime('Scheduled Date', required=True, )
    forin_lines_ids = fields.One2many(comodel_name="forin.purchase.lines", inverse_name="forin_id", string="",
                                      required=False, )
    picking_type_finish_id = fields.Many2one('stock.picking.type', domain=[('is_transients', '=', True)],
                                             default=_default_picking_type_id, string="Receive Operation Type",
                                             readonly=False)
    picking_type_sender_id = fields.Many2one('stock.picking.type', domain=[('is_senders', '=', True)],
                                             default=_default_sender_type_id,
                                             string="Send Operation Type", readonly=False)
    picking_count = fields.Integer(compute='compute_picking_count')
    purchase_count = fields.Integer(compute='compute_purchase_count')
    account_count = fields.Integer(compute='compute_account_count')

    def compute_picking_count(self):
        for record in self:
            record.picking_count = self.env['stock.picking'].search_count(
                [('origin', '=', self.name)])

    def compute_purchase_count(self):
        for record in self:
            record.purchase_count = self.env['purchase.order'].search_count(
                [('origin', '=', self.name)])

    def compute_account_count(self):
        for record in self:
            record.account_count = self.env['account.move'].search_count(
                [('invoice_origin', '=', self.name)])

    def get_account(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('invoice_origin', '=', self.name)],
            'context': "{'create': False}"
        }

    def get_purchase(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('origin', '=', self.name)],
            'context': "{'create': False}"
        }

    def get_picking(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Picking',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.name)],
            'context': "{'create': False}"
        }

    def state_onway(self):
        self.write({'state': 'atport'})
        stock = self.env['stock.picking']
        account = self.env['account.move']
        if self.forin_lines_ids:
            stock_obj = stock.create({
                'origin': self.name,
                'picking_type_id': self.picking_type_finish_id.id,
                'location_id': self.picking_type_sender_id.default_location_src_id.id,
                'location_dest_id': self.picking_type_finish_id.default_location_dest_id.id,
            })
            account_obj = account.create({
                'invoice_origin': self.name,
                'partner_id': self.partner_id.id,
                'currency_id': self.currency_id.id,
                'invoice_date': self.date_planned.date(),
                'move_type':  'in_invoice',
            })
            for line in self.forin_lines_ids:
                stock_obj.update({'move_ids_without_package': [(0, 0, {'name': line.product_id.name,
                                                                       'product_id': line.product_id.id,
                                                                       'picking_type_id': self.picking_type_finish_id.id,
                                                                       'location_id': self.picking_type_sender_id.default_location_src_id.id,
                                                                       'location_dest_id': self.picking_type_finish_id.default_location_dest_id.id,
                                                                       'product_uom': line.product_id.uom_id.id,
                                                                       'quantity_done': line.product_qty,
                                                                       'product_uom_qty': line.product_qty})]})
                account_obj.update({'invoice_line_ids': [(0, 0, {'name': line.product_id.name,
                                                               'product_id': line.product_id.id,
                                                               'price_unit': line.price_unit,
                                                               'quantity': line.product_qty})]})
            stock_obj.action_confirm()
            stock_obj.button_validate()
            account_obj.action_post()

    def state_inport(self):
        self.write({'state': 'onway'})

    def state_egyport(self):
        self.write({'state': 'egyport'})
        purchase = self.env['purchase.order']
        if self.forin_lines_ids:
            purchase_obj = purchase.create({
                'origin': self.name,
                'partner_id': self.partner_id.id,
                'currency_id': self.currency_id.id,
                'for_in': True,
                'date_planned': self.date_planned,
            })
            for line in self.forin_lines_ids:
                purchase_obj.update({'order_line': [(0, 0, {'name': line.product_id.name,
                                                            'product_id': line.product_id.id,
                                                            'product_uom': line.product_id.uom_id.id,
                                                            'price_unit': line.price_unit,
                                                            'product_qty': line.product_qty})]})
            purchase_obj.button_confirm()

    def state_delivered(self):
        self.write({'state': 'delivered'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'forin.purchase') or 'New'
        result = super(ForinPurchase, self).create(vals)
        return result


class ForinPurchaseLines(models.Model):
    _name = 'forin.purchase.lines'
    _rec_name = 'product_id'

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True, )
    product_qty = fields.Float('Quantity', default=1.0, digits='Product Unit of Measure', required=True)
    price_unit = fields.Float('Unit Price', required=True, store=True, related='product_id.standard_price',
                              readonly=False)
    price_subtotal = fields.Float(string="Subtotal", compute='_compute_price_subtotal', )
    forin_id = fields.Many2one(comodel_name="forin.purchase", string="", required=False, )

    @api.depends('product_id', 'product_qty', 'price_unit')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.product_qty * rec.price_unit


class StockPickingChecks(models.Model):
    _inherit = 'stock.picking.type'

    is_transients = fields.Boolean(string="Transient", )
    is_senders = fields.Boolean(string="Sender", )
