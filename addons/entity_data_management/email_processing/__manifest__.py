{
    'name': 'Email Processing',
    'version': '1.0',
    'summary': 'Email Processing Module',
    'license': 'LGPL-3',
    'author': 'Oddos Solutions LLC',
    'depends': ['base_entity_data'],  # Ensure this module is correctly named
    'data': [
        'views/email_processing_view.xml',  # Updated path to reflect that 'email_processing' is already the root
    ],
    'installable': True,
    'application': False,
    'description': """
    This module handles email processing for entity data management.
    Developed by Oddos Solutions LLC.
    """,
}
