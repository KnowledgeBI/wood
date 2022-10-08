# -*- coding: utf-8 -*-
{
    'name': "Invoice Adding Taxes",

    'summary': """
        Adding Taxes On Invoice Line Automatic
        """,

    'description': """
        Adding Taxes On Invoice Line Automatic
    """,

    'author': "Knowledge",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
