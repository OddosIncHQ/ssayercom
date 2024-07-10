{
    'name': 'SII Data Module',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Module for SII Data',
    'description': 'Handles SII Data',
    'depends': ['base', 'mail'],
    'data': [
        'security/sii_data_security.xml',
        'security/ir.model.access.csv',
        'views/sii_data_views.xml',
        'views/mail_activity_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
