{
    'name': 'Mail Message Viewer',
    'version': '17.0',
    'summary': 'Module to view incoming mail messages',
    'license': 'LGPL-3',
    'sequence': 1,
    'description': 'Custom module to view and manage incoming mail messages.',
    'category': 'Tools',
    'author': 'Oddos Solutions',
    'website': 'https://www.yourwebsite.com',
    'depends': ['base', 'mail'],
    'data': [
        'views/mail_message_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
