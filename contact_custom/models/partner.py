# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class ResPartner(models.Model):
    _inherit = 'res.partner'

    english_name = fields.Char(string="English Name", required=False, )
    type_id = fields.Many2one(comodel_name="partner.type", string="Type", required=False, )
    code = fields.Char(string="Code", required=False, )
    old_code = fields.Char(string="Old Code", required=False, )
    is_delivery_man = fields.Boolean()
    
    @api.model
    def create(self, vals):
        rec = super(ResPartner, self).create(vals)
        if rec.type_id and rec.type_id.sequence_id:
            code = rec.type_id.sequence_id.next_by_id()
            rec.code = "{}-{}".format(rec.type_id.prefix, code)
        return rec


class PartnerType(models.Model):
    _name = 'partner.type'
    _rec_name = 'name'
    _description = 'Partner Type'

    name = fields.Char(required=True)
    prefix = fields.Char(required=True)
    sequence_id = fields.Many2one(comodel_name="ir.sequence", string="Sequence")
    is_employee = fields.Boolean()

    @api.model
    def create(self, vals):
        rec = super(PartnerType, self).create(vals)
        if not rec.sequence_id:
            sequence_id = self.env['ir.sequence'].create({
                'name': rec.name,
                'padding': 6,
                'company_id': False,
            })
            rec.sequence_id = sequence_id.id
        return rec

    def write(self, vals):
        super(PartnerType, self).write(vals)
        if vals.get('name'):
            for rec in self:
                rec.sequence_id.name = rec.name
        return True

    def unlink(self):
        self.mapped('sequence_id').unlink()
        res = super(PartnerType, self).unlink()
        return res
