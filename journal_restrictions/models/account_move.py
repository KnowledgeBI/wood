""" Initialize Account Move """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountMove(models.Model):
    """
        Inherit Account Move:
         -
    """
    _inherit = 'account.move'

    def action_post(self):
        """ Override action_post """
        res = super(AccountMove, self).action_post()
        if self.journal_id in self.env.user.journal_ids:
            raise ValidationError('You does not access to confirm invoice !')
        return res
