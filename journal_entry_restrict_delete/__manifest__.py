# -*- coding: utf-8 -*-
{
    'name': "Journal Entry Restrict Deletion",

    'summary': """
        Journal Entry Restrict Deletion
        """,

    'description': """
        Journal Entry Restrict Deletion
    """,

    'author': "Knowledge",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account',
    'version': '12.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
    ],

    # always loaded
    'data': [
        'security/group.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
