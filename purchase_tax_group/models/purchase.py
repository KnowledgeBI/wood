# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp

from functools import partial
from odoo.tools.misc import formatLang, get_lang


# class PurchaseLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     discount = fields.Float(string="Discount", required=False, )


class Purchase(models.Model):
    _inherit = 'purchase.order'

    amount_by_group = fields.Binary(string="Tax amount by group",
                                    compute='_amount_by_group',
                                    help="type: [(name, amount, base, formated amount, formated base)]")

    @api.depends(
        'order_line.taxes_id',
        'order_line.price_unit',
        'order_line.product_qty',
        'order_line.product_id',
        'partner_id',
    )
    def _amount_by_group(self):
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
            res = {}
            for line in order.order_line:
                # price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
                price_reduce = line.price_unit
                taxes = line.taxes_id.compute_all(price_reduce, quantity=line.product_qty, product=line.product_id,
                                                  partner=order.partner_id)['taxes']
                for tax in line.taxes_id:
                    group = tax.tax_group_id
                    res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                    for t in taxes:
                        if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                            res[group]['amount'] += t['amount']
                            res[group]['base'] += t['base']
            res = sorted(res.items(), key=lambda l: l[0].sequence)
            order.amount_by_group = [(
                l[0].name, l[1]['amount'], l[1]['base'],
                fmt(l[1]['amount']), fmt(l[1]['base']),
                len(res),
            ) for l in res]
