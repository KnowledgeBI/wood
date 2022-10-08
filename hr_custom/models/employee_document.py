from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class HrEmployeeDocument(models.Model):
    _name = 'hr.employee.document'
    _inherit = ['hr.employee.document', 'portal.mixin', 'mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        related="employee_ref.company_id",
        store=True
    )

    def mail_reminder(self):
        employee_doc_expire_reminder = self.env.user.company_id.employee_doc_expire_reminder
        will_expired_document = self.env['hr.employee.document'].search([
            ('expiry_date', '>=', date.today()),
            ('expiry_date', '<=', date.today() + timedelta(days=employee_doc_expire_reminder)),
        ])
        group_id = self.env.ref("hr_custom.group_employee_document_expiry_reminder")
        users = group_id.users
        if will_expired_document and users:
            notify = self.env['user.notify']
            for doc in will_expired_document:
                msg = "Document: {} for Employee: {} will expired at {}".format(
                    doc.name,
                    doc.employee_ref.name,
                    doc.expiry_date
                )
                notify.send_notification(doc, users, msg)
