from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_custody = fields.Boolean('Custody?')