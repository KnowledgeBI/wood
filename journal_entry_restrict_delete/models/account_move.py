# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp

import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def unlink(self):
        if not self.env.user.has_group('journal_entry_restrict_delete.group_force_journal_entry_deletion'):
            raise exceptions.ValidationError('You not allowed to delete Journal Entry !')
        return super(AccountMove, self).unlink()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def unlink(self):
        if not self.env.user.has_group('journal_entry_restrict_delete.group_force_journal_entry_deletion'):
            raise exceptions.ValidationError('You not allowed to delete Journal Item !')
        return super(AccountMoveLine, self).unlink()
