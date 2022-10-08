""" Initialize Hr Employee """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrEmployee(models.Model):
    """
        Inherit Hr Employee:
         -
    """
    _inherit = 'hr.employee'

    created_partner_id = fields.Many2one(
        'res.partner'
    )

    @api.model
    def create(self, vals_list):
        """ Override create """
        # vals_list ={'field': value}  -> dectionary contains only new filled fields
        res = super(HrEmployee, self).create(vals_list)
        group = self.env['partner.type'].search([('is_employee', '=', True)], limit=1)
        partner = self.env['res.partner'].create({
            'name': res.name,
            'function': res.job_title.name if res.job_title else '',
            'mobile':res.work_phone or '',
            'type_id':group.id if group else '',
            'national_id':res.identification_id or ''
        })
        res.created_partner_id = partner.id
        return res