{
    'name': 'SII Data',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/sii_data_security.xml',  # Ensure this is the correct path
        'views/sii_data_views.xml',
    ],
    'demo': [],
    'installable': True,
}

