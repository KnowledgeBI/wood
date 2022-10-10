# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartnerCategory(models.Model):
    """
        Inherit Res Partner Category:
         -
    """
    _inherit = 'res.partner.category'

    discount = fields.Float()

    
class ResPartner(models.Model):
    _inherit = "res.partner"

    enable_default_discount = fields.Boolean()
    default_discount = fields.Float(string="Default Discount %")
    
    @api.onchange('category_id')
    def _onchange_category_id(self):
        """ category_id """
        for rec in self:
            if rec.category_id:
                if rec.category_id[0].discount:
                    rec.update({
                        'enable_default_discount': True,
                        'default_discount': rec.category_id[0].discount,
                    })

class SaleOrder(models.Model):
    _inherit = "sale.order"

    default_discount = fields.Float(string="Default Discount %")
    enable_default_discount = fields.Boolean(related="partner_id.enable_default_discount")

    @api.onchange("partner_id")
    def set_default_discount(self):
        if self.partner_id and self.enable_default_discount:
            self.default_discount = self.partner_id.default_discount
        else:
            self.default_discount = 0


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def set_default_discount(self):
        if self.product_id:
            self.discount = self.order_id.default_discount
        else:
            self.discount = 0


class AccountMove(models.Model):
    _inherit = "account.move"

    default_discount = fields.Float(string="Default Discount %")
    enable_default_discount = fields.Boolean(related="partner_id.enable_default_discount")

    @api.onchange("partner_id")
    def set_default_discount(self):
        if self.partner_id and self.enable_default_discount:
            self.default_discount = self.partner_id.default_discount
        else:
            self.default_discount = 0


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange("product_id")
    def set_default_discount(self):
        if self.product_id:
            self.discount = self.move_id.default_discount
        else:
            self.discount = 0


