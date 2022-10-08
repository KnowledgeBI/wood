""" Initialize Account Payment """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountPayment(models.Model):
    """
        Inherit Account Payment:
         -
    """
    _inherit = 'account.payment'

    def action_post(self):
        """ Override action_post """
        res = super(AccountPayment, self).action_post()
        if self.journal_id in self.env.user.journal_ids:
            raise ValidationError('You does not access to confirm invoice !')
        return res
