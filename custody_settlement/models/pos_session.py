""" Initialize Pos Session """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class PosSession(models.Model):
    """
        Inherit Pos Session:
         - 
    """
    _inherit = 'pos.session'
    #
    def action_pos_session_closing_control(self):
        """ Override action_pos_session_closing_control """
        res = super(PosSession, self).action_pos_session_closing_control()
        orders = self.order_ids
        payments = orders.mapped('payment_ids')
        moves = payments.mapped('account_move_id')
        # self.mapped('order_ids.payment_ids.account_move_id')
        return res

    # all_account_move_ids = fields.Many2many(
    #     'account.move',
    #     'move_payment_relation',
    #     'move_id',
    #     'payment_id',
    #     related='pos_payment_ids.account_move_id'
    # )
    # pos_payment_ids = fields.Many2many(
    #     'pos.payment',
    #     'order_payment_relation',
    #     'order_id',
    #     'payment_id',
    #     related='order_ids.payment_ids'
    # )