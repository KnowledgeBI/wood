# -*- coding: utf-8 -*-
{
    'name': "Hr Custom",
    'summary': """
        Hr Custom
        """,
    'description': """
        Hr Custom
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'hr',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'hr',
        'portal',
        'hr_contract',
        'oh_employee_documents_expiry',
        'user_notify',
        'hr_employee_service',
        'analytic',
        # 'crm',
        'hr_attendance',
        'hr_holidays',
    ],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/transfer_track.xml',
        'views/hr_employee.xml',
        'views/res_config.xml',
        'views/employee_document.xml',
        'views/work_number.xml',
        'views/hr_leave.xml',
        'views/hr_department.xml',
        'views/religion_views.xml',
        'views/hr_attendance.xml',
        'wizard/atm.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
