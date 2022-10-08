# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp


class TaxDepartment(models.Model):
    _name = 'tax.department'
    _description = 'Tax Department'

    name = fields.Char(string='Name', required=True, index=True)
    code = fields.Char(string='Code', required=True, copy=False)

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'Code must be unique!')
    ]
