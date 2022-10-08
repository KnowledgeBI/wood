{
    'name': 'Contact Custom',
    'version': '13.0.1.0.1',
    'Description': "Contact Custom",
    'depends': [
        'base','account','hr'
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/industry.xml',
        'views/tax_department.xml',
        'views/hr_employee.xml',

    ],
    'demo': [
    ],
    'images': [],
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}
