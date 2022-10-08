# -*- coding: utf-8 -*-
{
    'name': 'POS Customer Info on Receipt',
    'version': '1.0',
    'author': 'Preway IT Solutions',
    "sequence": 2,
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'summary': 'This module is allow to print customer info on pos receipt | Pos Receipt Customer Info | Customer Details on pos receipt',
    'description': """
  This module is allow to print customer info on pos receipt
    """,
    'data': [
        'views/pos_config_view.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'pw_pos_customer_details/static/src/xml/**/*',
        ],
    },
    'price': 10.0,
    'currency': "EUR",
    'application': True,
    'installable': True,
    "auto_install": False,
    "license": "LGPL-3",
    "images":["static/description/Banner.png"],
}

