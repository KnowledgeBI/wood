""" Initialize Analytic Account """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountAnalyticAccount(models.Model):
    """
        Inherit Account Analytic Account:
         -
    """
    _inherit = 'account.analytic.account'

    @api.model
    def create(self, vals_list):
        """ Override create """
        res = super(AccountAnalyticAccount, self).create(vals_list)
        if not self.env.user.has_group('create_analytic_group.group_create_analytic_account'):
            raise ValidationError('You can not create analytic account')
        return res
