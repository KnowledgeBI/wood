""" Initialize Assign Employee Pos """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AssignEmployeePos(models.Model):
    """
        Initialize Assign Employee Pos:
         -
    """
    _name = 'assign.employee.pos'
    _description = 'Assign Employee Pos'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one(
        'hr.employee',
        required=1
    )
    pos_config_id = fields.Many2one(
        'pos.config',
        required=1
    )
    is_assigned = fields.Boolean()

    def action_assign_employee_to_pos(self):
        """ Action Assign Employee To Pos """
        for rec in self:
            if rec.pos_config_id:
                if not rec.pos_config_id.module_pos_hr:
                    rec.pos_config_id.module_pos_hr = True
                rec.pos_config_id.write({
                    'employee_ids': rec.pos_config_id.employee_ids + rec.employee_id
                })
                rec.is_assigned = True