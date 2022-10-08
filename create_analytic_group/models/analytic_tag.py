""" Initialize Analytic Tag """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountAnalyticTag(models.Model):
    """
        Inherit Account Analytic Tag:
         -
    """
    _inherit = 'account.analytic.tag'

    @api.model
    def create(self, vals_list):
        """ Override create """
        res = super(AccountAnalyticTag, self).create(vals_list)
        if not self.env.user.has_group('create_analytic_group.group_create_analytic_tag'):
            raise ValidationError('You can not create analytic account')
        return res
