""" Initialize Account Move """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountJournal(models.Model):
    """
        Inherit Account Move:
         - 
    """
    _inherit = 'account.journal'

    can_see = fields.Boolean(
        compute='_compute_can_see'
    )

    def _compute_can_see(self):
        """ Compute can_see value """
        for rec in self:
            if rec.id in self.env.user.journal_ids:
                rec.can_see = True
            else:
                rec.can_see = False
