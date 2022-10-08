
{
    'name': 'Trial Balance Report',
    'summary': 'Trial Balance Report',
    'author': "knowledge BI , Mahmoud Elfeky",
    'company': 'knowledge BI',
    'website': "https://www.knowledgebi.net/",
    'version': '15.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'analytic',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'report/',
        'wizard/trial_report.xml',
        'views/analytic_account.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

