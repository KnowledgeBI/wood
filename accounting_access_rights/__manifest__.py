
{
    'name': 'Accounting Access Rights',
    'summary': 'Accounting Access Rights',
    'author': "knowledge BI , Mahmoud Elfeky",
    'company': 'knowledge BI',
    'website': "https://www.knowledgebi.net/",
    'version': '15.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'security/security.xml',
        # 'report/',
        # 'wizard/',
        'views/account_move.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

