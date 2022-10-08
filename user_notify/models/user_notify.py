# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountMoveBill(models.TransientModel):
    _name = 'user.notify'
    _description = 'User Notify'

    def send_notification(self, obj, users, msg):
        try:
            if users:
                self.env['mail.message'].create({
                    'message_type': "notification",
                    "subtype_id": self.env.ref("mail.mt_comment").id,
                    'body': "Dear Sir<br></br>" + msg + "<br></br> Best Regards",
                    'subject': obj.name,
                    'partner_ids': [(4, user.partner_id.id) for user in users],
                    'needaction_partner_ids': [(4, user.partner_id.id) for user in users],
                    'model': obj._name,
                    'res_id': obj.id,
                })
        except Exception as e:
            _logger.error(e)

    def create_activity(self, obj, users, summary):
        for user in users:
            try:
                model_id = self.env['ir.model']._get(obj._name).id
                self.env['mail.activity'].sudo().create({
                    'res_id': obj.id,
                    'res_model_id': model_id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': summary,
                    'user_id': user.id,
                    'date_deadline': fields.date.today()
                })
            except Exception as e:
                _logger.error(e)
                continue

    def done_activity(self, obj):
        model_id = self.env['ir.model']._get(obj._name).id
        activities = self.env['mail.activity'].search([
            ('res_id', '=', obj.id),
            ('res_model_id', '=', model_id),
        ])
        if activities:
            activities.sudo().action_done()
