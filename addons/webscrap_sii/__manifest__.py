{
    'name': 'Web Scrap SII',
    'version': '1.0',
    'summary': 'Module for SII Web Scraping integration',
    'description': 'This module integrates a web scraping feature for SII within the Odoo website.',
    'author': 'Your Name',
    'category': 'Website',
    'depends': ['website', 'web'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'webscrap_sii/static/src/js/sii_login.js',
            'webscrap_sii/static/src/scss/style.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',  # Add this line to specify the license
}
