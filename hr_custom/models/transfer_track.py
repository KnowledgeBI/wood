# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp


class TransferTracking(models.Model):
    _name = 'transfer.track'
    _rec_name = 'employee_id'
    _description = 'Transfer Tracking'

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True, )
    company_id = fields.Many2one(comodel_name="res.company", string="Company", related="employee_id.company_id")
    job_id = fields.Many2one(comodel_name="hr.job", string="Job")

    date = fields.Date(string="", required=True, default=date.today())

    @api.constrains('job_id')
    def _check_data(self):
        for line in self:
            if not line.job_id:
                raise exceptions.ValidationError('Job Mandatory !')
