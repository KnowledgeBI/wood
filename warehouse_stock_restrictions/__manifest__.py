# -*- coding: utf-8 -*-

{
    'name': "Warehouse Restrictions",

    'summary': """
         Warehouse and Stock Locations, Picking types and picking Restriction on Users.""",

    'description': """
        This Module Restricts the User from Accessing Warehouse and Process Stock Moves other than allowed to Warehouses and Stock Locations.
    """,

    'author': " Techspawn Solutions",

    'category': 'Warehouse',
    'version': '14.0.1.0',

    'depends': ['base', 'stock', 'sale_stock'],

    'data': [
        'security/security.xml',
        'views/users.xml',
    ],
    "images": [
        'static/description/banner.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
