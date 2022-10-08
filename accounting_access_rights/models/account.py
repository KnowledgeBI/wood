""" Initialize Account """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountAccount(models.Model):
    """
        Inherit Account Account:
         -
    """
    _inherit = 'account.account'

    @api.model
    def create(self, values):
        if not self.env.user.has_group('accounting_access_rights.group_create_chart_of_account'):
            raise AccessError(_('You Don Not have Access to Create Account'))

        return super(AccountAccount, self).create(values)


