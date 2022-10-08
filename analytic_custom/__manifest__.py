{
    'name': 'Analytic Custom',
    'summary': 'Analytic Custom',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'website': '',
    'author': "Eng-Mahmoud Ramadan",
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'account',
        'analytic',
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/analytic.xml',
        'views/analytic_group.xml',
        'views/account_account_view.xml',
    ],
}
