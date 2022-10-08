# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp


class ATM(models.TransientModel):
    _name = 'employee.atm'
    _description = 'Employee ATM'

    code = fields.Char(string="ATM Code", required=True, )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=False, )

    def action_confirm(self):
        self.employee_id.code = self.code
