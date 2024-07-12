{
    'name': 'Custom CSV Import',
    'version': '1.0',
    'summary': 'Module to import and store CSV data',
    'description': 'Custom module to import CSV data and store it in respective fields for historical tracking.',
    'author': 'Your Name',
    'category': 'Custom',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/csv_data_views.xml',
    ],
    'installable': True,
    'application': True,
}
