# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp

from math import fabs
from dateutil.relativedelta import relativedelta


class ResUsers(models.Model):
    _inherit = 'res.users'

    job_title = fields.Many2one(related='employee_id.job_title', readonly=False, related_sudo=False)
    certificate = fields.Many2one(related='employee_id.certificate', readonly=False, related_sudo=False)
    study_field = fields.Many2one(related='employee_id.study_field', readonly=False, related_sudo=False)
    study_school = fields.Many2one(related='employee_id.study_school', readonly=False, related_sudo=False)

    @api.constrains('groups_id')
    def _check_one_user_type(self):
        """We check that no users are both portal and users (same with public).
           This could typically happen because of implied groups.
        """
        user_types_category = self.env.ref('base.module_category_user_type', raise_if_not_found=False)
        user_types_groups = self.env['res.groups'].search(
            [('category_id', '=', user_types_category.id)]) if user_types_category else False
        if user_types_groups:  # needed at install
            if self._has_multiple_groups(user_types_groups.ids):
                raise ValidationError(_('The user cannot have more than one user types.'))

    def _has_multiple_groups(self, group_ids):
        """The method is not fast if the list of ids is very long;
           so we rather check all users than limit to the size of the group
        :param group_ids: list of group ids
        :return: boolean: is there at least a user in at least 2 of the provided groups
        """
        # if group_ids:
        #     args = [tuple(group_ids)]
        #     if len(self.ids) == 1:
        #         where_clause = "AND r.uid = %s"
        #         args.append(self.id)
        #     else:
        #         where_clause = ""  # default; we check ALL users (actually pretty efficient)
        #     query = """
        #             SELECT 1 FROM res_groups_users_rel WHERE EXISTS(
        #                 SELECT r.uid
        #                 FROM res_groups_users_rel r
        #                 WHERE r.gid IN %s""" + where_clause + """
        #                 GROUP BY r.uid HAVING COUNT(r.gid) > 1
        #             )
        #     """
        #     self.env.cr.execute(query, args)
        #     return bool(self.env.cr.fetchall())
        # else:
        #     return False
        return False
