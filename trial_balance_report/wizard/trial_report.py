""" Initialize Trial Report """

import pytz
import base64
import io
from io import BytesIO
from psycopg2.extensions import AsIs
from babel.dates import format_date, format_datetime, format_time
from odoo import fields, models, api, _, tools, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from dateutil.relativedelta import relativedelta
from odoo.fields import Datetime as fieldsDatetime
import calendar
from odoo import http
from odoo.http import request
from odoo import tools

import logging

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

LOGGER = logging.getLogger(__name__)


class TrialBalance(models.TransientModel):
    """
        Initialize Trial Balance:
         -
    """
    _name = 'trial.balance'
    _description = 'Trial Balance'

    date_from = fields.Date()
    date_to = fields.Date()
    excel_sheet = fields.Binary('Download Report')
    excel_sheet_name = fields.Char(string='Name', size=64)
    analytic_account_ids = fields.Many2many(
        'account.analytic.account'
    )
    target_move = fields.Selection(
        [("posted", "All Posted Entries"), ("all", "All Entries")],
        string="Target Moves",
        required=True,
        default="posted",
    )

    def get_report_data(self):
        if self.date_from and self.date_to and self.date_from >= self.date_to:
            raise ValidationError(_('Date from must be before date to!'))
        data = []
        accounts = self.env['account.account'].search([])
        if self.target_move == 'posted':
            all_move_lines = self.env['account.move.line'].search([
                ('analytic_account_id', '!=', False),
                ('date', '<=', self.date_to),
                ('date', '>=', self.date_from),
                ('parent_state', '=', 'posted'),
            ])
        else:
            all_move_lines = self.env['account.move.line'].search([
                ('analytic_account_id', '!=', False),
                ('date', '<=', self.date_to),
                ('date', '>=', self.date_from),
                ('parent_state', 'in', ['posted', 'draft'])
            ])

        if self.analytic_account_ids:
            analytic_accounts = self.analytic_account_ids
        else:
            analytic_accounts = self.env['account.analytic.account'].search([])
        for account in accounts:
            for analytic in analytic_accounts:
                moves = all_move_lines.filtered(lambda x: x.account_id == account and x.analytic_account_id == analytic)
                if moves:
                    code = account.code
                    account_name = account.name
                    analytic_code = analytic.code
                    analytic_name = analytic.name
                    debit = sum(moves.mapped('debit'))
                    credit = sum(moves.mapped('credit'))
                    balance = debit - credit
                    data.append((code, account_name, analytic_code, analytic_name, balance))
            if self.target_move == 'posted':
                account_move_lines = self.env['account.move.line'].search([
                    ('analytic_account_id', '=', False),
                    ('account_id', '=', account.id),
                    ('date', '<=', self.date_to),
                    ('date', '>=', self.date_from),
                    ('parent_state', '=', 'posted'),
                ])
            else:
                account_move_lines = self.env['account.move.line'].search([
                    ('analytic_account_id', '=', False),
                    ('account_id', '=', account.id),
                    ('date', '<=', self.date_to),
                    ('date', '>=', self.date_from),
                    ('parent_state', 'in', ['posted', 'draft'])
                ])

            if account_move_lines:
                code = account.code
                account_name = account.name
                analytic_code = ' '
                analytic_name = ' '
                debit = sum(account_move_lines.mapped('debit'))
                credit = sum(account_move_lines.mapped('credit'))
                balance = debit - credit
                data.append((code, account_name, analytic_code, analytic_name, balance))
        return data

    def action_print_excel_file(self):
        self.ensure_one()
        data = self.get_report_data()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        TABLE_HEADER = workbook.add_format({
            'bold': 1,
            'font_name': 'Tahoma',
            'border': 0,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
        })

        header_format = workbook.add_format({
            'bold': 1,
            'font_name': 'Aharoni',
            'border': 0,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
            'bg_color': '#c3c6c5',
        })

        TABLE_HEADER_Data = TABLE_HEADER
        TABLE_HEADER_Data.num_format_str = '#,##0.00_);(#,##0.00)'
        STYLE_LINE = workbook.add_format({
            'border': 0,
            'align': 'center',
            'valign': 'vcenter',
        })

        TABLE_data = workbook.add_format({
            'bold': 1,
            'font_name': 'Aharoni',
            'border': 0,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
        })
        TABLE_data.num_format_str = '#,##0.00'
        TABLE_data_tolal_line = workbook.add_format({
            'bold': 1,
            'font_name': 'Aharoni',
            'border': 1,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
            'bg_color': 'yellow',
        })

        TABLE_data_tolal_line.num_format_str = '#,##0.00'
        TABLE_data_o = workbook.add_format({
            'bold': 1,
            'font_name': 'Aharoni',
            'border': 0,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
        })
        STYLE_LINE_Data = STYLE_LINE
        STYLE_LINE_Data.num_format_str = '#,##0.00_);(#,##0.00)'

        worksheet = workbook.add_worksheet('Trial Balance with Analytical Account')

        worksheet.set_column(0, 16, 15)
        row = 0
        col = 0
        worksheet.write(row,col,'Trial Balance with Analytical Account',header_format)
        row += 1
        worksheet.write(row,col,
                        str(self.env.company.name),header_format)
        row += 1
        worksheet.write(row,col,_(' From'),header_format)
        col += 1
        worksheet.write(row,col,str(self.date_from),header_format)
        col += 1
        worksheet.write(row,col,_(' To'),header_format)
        col += 1
        worksheet.write(row,col,str(self.date_to),header_format)
        row += 2
        col = 0
        worksheet.write(row, col, _('Code'), header_format)
        col += 1
        worksheet.write(row, col, _('Account Name'), header_format)
        col += 1
        worksheet.write(row, col, _('Analytical Code'), header_format)
        col += 1
        worksheet.write(row, col, _('Analytical Name'), header_format)
        col += 1
        worksheet.write(row, col, _('Balance'), header_format)
        for d in data:
            row += 1
            col = 0
            worksheet.write(row, col, str(d[0]), STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, d[1], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, d[2], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, d[3], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, d[4], STYLE_LINE_Data)

        if data:
            self.excel_sheet_name = 'Trial Balance with Analytical Account'
            workbook.close()
            output.seek(0)
            self.excel_sheet = base64.encodestring(output.read())
            self.excel_sheet_name = str(self.excel_sheet_name) + '.xlsx'
            return {
                'type': 'ir.actions.act_url',
                'name': 'sales Report',
                'url': '/web/content/trial.balance/%s/excel_sheet/Trial Balance with Analytical Account.xlsx?download=true' % (
                    self.id),
                'target': 'self'
            }

        else:

            view_action = {
                'name': _(' Trial Balance Report'),
                'view_mode': 'form',
                'res_model': 'trial.balance',
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                'target': 'new',
                'context': self.env.context,
            }

            return view_action

