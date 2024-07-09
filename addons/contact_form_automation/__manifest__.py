{
    'name': 'Contact Form Automation',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Automate contact form actions',
    'description': 'Automate login and form submission on external website.',
    'author': 'Your Name',
    'website': 'https://www.ssayer.com',
    'depends': ['base', 'website'],
    'data': [
        'views/contact_form_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
