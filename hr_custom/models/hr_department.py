# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp

from math import fabs
from dateutil.relativedelta import relativedelta


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    is_section = fields.Boolean('Section')