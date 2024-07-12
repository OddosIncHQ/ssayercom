{
    'name': 'SII Data Module',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Module for managing SII data',
    'description': 'Handles custom functionalities for SII data',
    'depends': ['base', 'mail_activity'],  # Asegúrate de incluir 'mail' o 'mail_activity' como dependencia
    'data': [
        'security/sii_data_security.xml',
        'views/sii_data_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
