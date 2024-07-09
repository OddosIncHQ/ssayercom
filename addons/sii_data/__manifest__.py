{
    'name': 'SII Data Module',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Module for SII Data',
    'description': 'Handles SII Data',
    'depends': ['base'],
    'data': [
        'views/sii_data_views.xml',
        'security/ir.model.access.csv',
        # Add other data files here
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
