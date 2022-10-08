# -*- coding: utf-8 -*-
{
    'name': "custody_settlement",

    'summary': """
        custody_settlement""",

    'description': """
      custody_settlement
        
    """,
    'version': '14.0.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'account',
                'hr',
                'sales_team',
                'point_of_sale',
                'pos_hr',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/account_move_view.xml',
        'views/assign_employee_pos.xml',
        'views/menu.xml',
        # 'views/sales_team.xml',
        'views/account_journal_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
