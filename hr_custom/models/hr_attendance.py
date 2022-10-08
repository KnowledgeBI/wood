# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp

from math import fabs
from dateutil.relativedelta import relativedelta


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    check_in_date = fields.Date('Check Date', compute='_compute_check_data')
    check_in_day = fields.Char('Check Day', compute='_compute_check_data')

    @api.depends('check_in')
    def _compute_check_data(self):
        for rec in self:
            if rec.check_in:
                rec.check_in_date = rec.check_in.date()
                rec.check_in_day = rec.check_in.strftime('%A')
            else:
                rec.check_in_date = False
                rec.check_in_day = False
