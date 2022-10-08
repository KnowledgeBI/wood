""" Initialize Account Bank Statement """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountBankStatement(models.Model):
    """
        Inherit Account Bank Statement:
         -
    """
    _inherit = 'account.bank.statement'

    def button_post(self):
        """ Override action_post """
        res = super(AccountBankStatement, self).button_post()
        if self.journal_id not in self.env.user.journal_ids:
            raise ValidationError('You does not access to confirm invoice !')
        return res
