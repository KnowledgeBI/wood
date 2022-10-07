
{
    'name': 'Routes Addon',
    'summary': 'Routes Addon',
    'author': "knowledge BI , Mahmoud Elfeky",
    'company': 'knowledge BI',
    'website': "https://www.knowledgebi.net/",
    'version': '15.0.0.1.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'sale',
        'fleet',
        'hr',
        'stock',
        'sale_stock',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/sale_order.xml',
        'views/sale_route.xml',
        'views/stock_picking.xml',
        'data/ir_sequence.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

