# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp

from math import fabs
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    state = fields.Selection(string="Job Status", selection=[
        ('at_work', 'At Work'),
        ('resignation', 'Resignation'),
        ('ending_service', 'Ending Service'),
        ('leaving_work', 'Leaving Work'),
        ('death', 'Death'),
    ], required=False, default='at_work', groups="hr.group_hr_user")
    state_id = fields.Many2one(comodel_name="res.country.state",
                               string="State",
                               related="address_home_id.state_id",
                               store=True, groups="hr.group_hr_user")
    job_title = fields.Many2one(comodel_name="hr.job.title", groups="hr.group_hr_user")
    is_special_need = fields.Boolean(string="People with special needs", groups="hr.group_hr_user")
    code = fields.Char(string="Employee Code", required=False, groups="hr.group_hr_user")
    new_field = fields.Float(string="", required=False, groups="hr.group_hr_user")
    certificate = fields.Many2one(comodel_name="hr.qualification", groups="hr.group_hr_user")
    certificate_year = fields.Char(string="", required=False, groups="hr.group_hr_user")
    arabic_name = fields.Char(string="Arabic Name", required=False, groups="hr.group_hr_user")
    religion = fields.Many2one('religion.religion', string="Religion", required=False, groups="hr.group_hr_user")
    section_id = fields.Many2one('hr.department', string='Section', groups="hr.group_hr_user")
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete='set null',
                                          check_company=True)
    # sector_id = fields.Many2one('crm.team', string='Sector')
    collar_workers = fields.Selection(string="Collar Workers", selection=[
        ('white', 'White'),
        ('blue', 'Blue'),
    ], required=False, groups="hr.group_hr_user")
    military_state = fields.Selection(string="Military State", selection=[
        ('temporary_exemption', 'إعفاء مؤقت'),
        ('final_exemption', 'إعفاء نهائى'),
        ('military', 'قوات مسلحه'),
        ('unknown', 'لم يصبه الدور'),
        ('undefined', 'غير محدد'),
        ('not_required', 'غير مطلوب'),
    ], required=False, groups="hr.group_hr_user")
    retirement_date = fields.Date(string='Retirement Date', compute='_compute_retirement_date', store=True,
                                  groups="hr.group_hr_user")
    identification_start_date = fields.Date(string='ID Start Date', groups="hr.group_hr_user")
    identification_end_date = fields.Date(string='ID End Date', groups="hr.group_hr_user")

    # TODO:Insurance fields
    insured = fields.Boolean(string="Insured", groups="hr.group_hr_user")
    currency_id = fields.Many2one(comodel_name="res.currency", related="company_id.currency_id", store=True,
                                  groups="hr.group_hr_user")
    # TODO:Private medical insurance
    insurance_level = fields.Selection(selection=[
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    ], required=False, groups="hr.group_hr_user")
    # TODO:Governmental Medical Insurance
    governmental_card_number = fields.Char(string="Governmental Card Number", required=False, groups="hr.group_hr_user")
    full_insurance_id = fields.Char(string="Full Insurance ID", compute="calc_full_insurance", store=True,
                                    groups="hr.group_hr_user")

    @api.depends('birthday')
    def _compute_retirement_date(self):
        for rec in self:
            retirement_date = False
            if rec.birthday:
                birthday = rec.birthday
                retirement_date = birthday.replace(year=birthday.year + 60)
            rec.retirement_date = retirement_date

    @api.depends('governmental_card_number', 'company_id.insurance_id')
    def calc_full_insurance(self):
        for emp in self:
            insurance = ""
            if emp.company_id.insurance_id:
                insurance += emp.company_id.insurance_id + "/"
            if emp.governmental_card_number:
                insurance += emp.governmental_card_number
            emp.full_insurance_id = insurance

    # TODO:Social Insurance
    social_insurance_id = fields.Char(string="Social Insurance ID", required=False, groups="hr.group_hr_user")
    social_join_date = fields.Date(string="Social Join Date", required=False, groups="hr.group_hr_user")
    social_insurance_amount = fields.Monetary(string="Social Insurance", required=False, groups="hr.group_hr_user")
    social_insurance_type_id = fields.Many2one(comodel_name="social.insurance.type", string="Social Insurance Type",
                                               required=False, groups="hr.group_hr_user")
    actual_social_insurance_amount = fields.Monetary(string="Actual Social Insurance",
                                                     compute="calc_actual_social_insurance_amount", store=True,
                                                     groups="hr.group_hr_user")

    @api.depends('social_insurance_amount', 'social_insurance_type_id.percent')
    def calc_actual_social_insurance_amount(self):
        for emp in self:
            if emp.social_insurance_type_id:
                emp.actual_social_insurance_amount = emp.social_insurance_type_id.percent / 100 * emp.social_insurance_amount
            else:
                emp.actual_social_insurance_amount = emp.social_insurance_amount

    #########################################################
    number_ids = fields.One2many(comodel_name="hr.employee.number", inverse_name="employee_id",
                                 string="",
                                 required=False, groups="hr.group_hr_user")

    transfer_tracing_ids = fields.One2many(comodel_name="transfer.track",
                                           inverse_name="employee_id",
                                           string="Transfer Tracking",
                                           required=False, groups="hr.group_hr_user")

    # TODO:Age Fields
    age = fields.Float(
        string='Age',
        readonly=True,
        compute='_compute_age',
        help='Age in days', groups="hr.group_hr_user"
    )
    study_field = fields.Many2one(comodel_name="hr.study.field", groups="hr.group_hr_user")
    study_school = fields.Many2one(comodel_name="hr.study.school", groups="hr.group_hr_user")

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday and date.today() > record.birthday:
                age = relativedelta(
                    date.today(),
                    record.birthday
                )
                record.age = age.years + (age.months / 12)
            else:
                record.age = 0

    _sql_constraints = [
        ('unique_identification', 'UNIQUE(identification_id)', 'Employee Identification Is Unique ! ')
    ]

    @api.onchange('job_id')
    def _onchange_job_id(self):
        if self.job_id:
            pass

    def action_resignation(self):
        self.check_dates()
        self.write({
            'active': False,
            'state': 'resignation',
        })

    def action_ending_service(self):
        self.check_dates()
        self.write({
            'active': False,
            'state': 'ending_service',
        })

    def action_leaving_work(self):
        self.check_dates()
        self.write({
            'active': False,
            'state': 'leaving_work',
        })

    def action_death(self):
        self.check_dates()
        self.write({
            'active': False,
            'state': 'death',
        })

    def action_at_work(self):
        self.write({
            'state': 'at_work',
            'service_termination_date': False,
            'service_hire_date': date.today(),
        })

    def check_dates(self):
        if not self.service_hire_date:
            raise exceptions.ValidationError('Please Set Work Hire Date !')
        if not self.service_termination_date:
            raise exceptions.ValidationError('Please Set Work Termination Date !')

    def action_atm(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('ATM Employee Code'),
            'res_model': 'employee.atm',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_id': self.id
            },
        }


class JobTitle(models.Model):
    _name = 'hr.job.title'
    _rec_name = 'name'
    _description = 'Job Title'

    name = fields.Char(required=True)


class Qualification(models.Model):
    _name = 'hr.qualification'
    _rec_name = 'name'
    _description = 'Qualification'

    name = fields.Char(required=True)


class Numbers(models.Model):
    _name = 'hr.employee.number'
    _rec_name = 'number'
    _description = 'Employee Number'

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=False, )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        related="employee_id.company_id",
        store=True
    )
    carrier = fields.Selection(selection=[
        ('vodafone', 'Vodafone'),
        ('etisalat', 'Etisalat'),
        ('orange', 'Orange'),
        ('we', 'We'),
    ], required=True)

    type = fields.Selection(selection=[
        ('data', 'Data'),
        ('normal', 'normal'),
    ], required=True)
    number = fields.Char(string="Number", required=True, )
    date = fields.Date(string="", required=True, )
    current_no = fields.Boolean(string="Current No", )
    operating_type_id = fields.Many2one(comodel_name="work.number.operating.type",
                                        string="Operating Type",
                                        required=True, )

    @api.constrains('current_no')
    def _check_current_no(self):
        for rec in self:
            if rec.current_no:
                rec.employee_id.mobile_phone = rec.number


class OperationType(models.Model):
    _name = 'work.number.operating.type'
    _rec_name = 'name'
    _description = 'Work Number Operating Type'

    name = fields.Char(string="", required=False, )
    carrier = fields.Selection(selection=[
        ('vodafone', 'Vodafone'),
        ('etisalat', 'Etisalat'),
        ('orange', 'Orange'),
        ('we', 'We'),
    ], required=True)
    type = fields.Selection(selection=[
        ('data', 'Data'),
        ('normal', 'normal'),
    ], required=True)


class SocialInsuranceType(models.Model):
    _name = 'social.insurance.type'
    _rec_name = 'name'
    _description = 'Social Insurance Type'

    name = fields.Char(string="", required=True, )
    percent = fields.Float(string="Percent", required=True)


class StudyField(models.Model):
    _name = 'hr.study.field'
    _rec_name = 'name'
    _description = 'Study Field'

    name = fields.Char(required=True)


class School(models.Model):
    _name = 'hr.study.school'
    _rec_name = 'name'
    _description = 'Study School'

    name = fields.Char(required=True)
