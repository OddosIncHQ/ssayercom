{
    'name': 'Contact Form Automation',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Automate contact form tax information submissions',
    'description': 'Module to automate handling of contact form tax information submissions',
    'author': 'Oddos Solutions LLC',
    'depends': ['website_form'],
    'data': [
        'security/ir.model.access.csv',
        'views/contact_form_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'icon': '/static/mojologo.png', 
}
