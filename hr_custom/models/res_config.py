# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp


class ResCompany(models.Model):
    _inherit = 'res.company'

    employee_doc_expire_reminder = fields.Integer(string='Employee Document Expire Reminder')
    insurance_id = fields.Char(string='Insurance Id')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    employee_doc_expire_reminder = fields.Integer(string='Employee Document Expire Reminder',
                                                  related="company_id.employee_doc_expire_reminder",
                                                  readonly=False)
    insurance_id = fields.Char(string='Insurance Id',
                               related='company_id.insurance_id',
                               readonly=False)
