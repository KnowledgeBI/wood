""" Initialize Crm Team """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class CrmTeam(models.Model):
    """
        Inherit Crm Team:
         -
    """
    _inherit = 'crm.team'

    custody_journal_id = fields.Many2one('account.journal', 'Custody Journal')
