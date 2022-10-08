# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError, Warning


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('industry_id')
    def onchange_field_industry_id(self):
        self.property_account_position_id = self.industry_id.fiscal_position_id.id

    national_id = fields.Char('National ID')
    national_file = fields.Binary('National ID', tracking=True)
    face_national_file = fields.Binary('Face National ID', tracking=True)
    back_national_file = fields.Binary('Back National ID', tracking=True)
    filename1 = fields.Char()
    mark_as_not_required = fields.Boolean('Mark As Not required')
    commercial_no = fields.Char('Commercial No.')
    commercial_reg = fields.Many2many('ir.attachment', 'partner_attach_commercial_rel', 'attach_id', 'partner_id',
                                      tracking=True)
    commercial_reg_expiry = fields.Date('Commercial Registration No. Expiry Date')
    filename2 = fields.Char()

    vat = fields.Char('Tax ID')

    # tax_id = fields.Char('Tax ID',readonly=True)

    tax_id_expiry = fields.Date('Tax ID Expiry Date')
    tax_card = fields.Many2many('ir.attachment', 'partner_attach_tax_rel', 'attach_id', 'partner_id',
                                tracking=True)
    filename3 = fields.Char()

    tax_file = fields.Char('Tax File')
    tax_dep = fields.Char(string='Tax Department')
    tax_department_id = fields.Many2one('tax.department', string='Tax Department')
    other_attachment_ids = fields.Many2many('ir.attachment', 'partner_attach_rel', 'attach_id', 'partner_id',
                                            tracking=True)
    english_name = fields.Char(string="English Name", required=False, )

    arabic_name = fields.Char(string="Arabic Name", required=False, )
    type_id = fields.Many2one(comodel_name="partner.type", string="Group", required=False, )
    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
                                                  string="Account Payable",
                                                  domain="[('deprecated', '=', False), ('company_id', '=', current_company_id)]",
                                                  help="This account will be used instead of the default one as the payable account for the current partner",
                                                  required=True)
    property_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
                                                     string="Account Receivable",
                                                     domain="[('deprecated', '=', False), ('company_id', '=', current_company_id)]",
                                                     help="This account will be used instead of the default one as the receivable account for the current partner",
                                                     required=True)

    @api.onchange('type_id')
    def onchange_type_id(self):
        self.category_id = self.type_id.category_ids.ids

    code = fields.Char(string="Code", required=False, )
    old_code = fields.Char(string="Old Code", required=False, )
    city = fields.Char(required=True)

    @api.model
    def create(self, vals):
        rec = super(Partner, self).create(vals)
        if rec.type_id and rec.type_id.sequence_id:
            code = rec.type_id.sequence_id.next_by_id()
            rec.code = "{}-{}".format(rec.type_id.prefix, code)
            rec.ref = rec.code
        return rec

    @api.constrains('mobile')
    def _check_mobile(self):
        """ Validate mobile """
        for rec in self:
            partner = self.env['res.partner'].search(
                [('mobile', '=', rec.mobile)]
            )
            if len(partner) > 1:
                raise ValidationError(_('Mobile Number Is Repeated On Partner %s') %partner[-1].name)

    @api.constrains('commercial_reg', 'tax_card')
    def _constrain_commercial_tax_card_attachment(self):
        for rec in self:
            if not rec.mark_as_not_required and rec.company_type == 'company':
                if not rec.commercial_reg:
                    raise exceptions.ValidationError(_('Please Add Commercial Reg File.'))
                if not rec.tax_card:
                    raise exceptions.ValidationError(_('Please Add Tax Card File.'))

    @api.constrains('commercial_no', 'national_id', 'vat', 'tax_file')
    def _check_commercial_no_national_id(self):
        for rec in self:
            if rec.commercial_no:
                if not rec.commercial_no.isdigit():
                    raise exceptions.ValidationError('Can not accept special character in commercial no')
                # if len(rec.commercial_no) != 5:
                #     raise exceptions.ValidationError('Commercial no should be 5 numbers')

            if rec.national_id:
                if not rec.national_id.isdigit():
                    raise exceptions.ValidationError('Can not accept character in national id.')
                if len(rec.national_id) != 14:
                    raise exceptions.ValidationError('National ID should be 14 numbers')

            if rec.vat:
                if not rec.vat.isdigit():
                    raise exceptions.ValidationError('Can not accept character in Tax ID.')
                if len(rec.vat) != 9:
                    raise exceptions.ValidationError('Tax ID  should be 9 numbers')

            if rec.tax_file:
                if not rec.tax_file.isdigit():
                    raise exceptions.ValidationError('Can not accept character in Tax File.')
                if len(rec.tax_file) != 14:
                    raise exceptions.ValidationError('Tax File  should be 14 numbers')

    def check_special_char(self, string):
        accepted_char = '1234567890'
        has_special_char = False
        for char in string:
            if char not in accepted_char:
                has_special_char = True
                break
        return has_special_char


class PartnerType(models.Model):
    _name = 'partner.type'
    _rec_name = 'name'
    _description = 'Partner Type'

    name = fields.Char(required=True)
    prefix = fields.Char(required=True)
    sequence_id = fields.Many2one(comodel_name="ir.sequence", string="Sequence")
    category_ids = fields.Many2many('res.partner.category', column1='partner_id',
                                    column2='partner_type_id', string='Tags')
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
