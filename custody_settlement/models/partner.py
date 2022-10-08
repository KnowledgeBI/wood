# -*- coding: utf-8 -*-
# from odoo import models, fields, api, exceptions, _
# from datetime import date, datetime, time, timedelta
# from odoo.fields import Date, Datetime
# from odoo.tools import float_compare
# class Partner(models.Model):
#     _inherit = 'res.partner'
#
#     is_employee_partner = fields.Boolean(string="Employee Contact",compute='check_employee_contact',store=True )
#     def check_employee_contact(self):
#         employees = self.env['hr.employee'].search([])
#         employee_ids = employees.mapped('user_id').mapped('partner_id').ids
#         for partner in self.search([]):
#                 partner.is_employee_partner = partner.id in employee_ids