{
    'name': "Conexiones bancarias para Chile y México",

    'summary': """
        Conexión de Odoo con los bancos de Chile y México
        """,

    'description': """
        Módulo que conecta Odoo con los bancos en Chile y México para registrar las cartolas bancarias automáticamente
    """,
    "support": "javier@nndeveloper.com",
    "price": "41",
    "currency": "USD",
    'author': "Javier López Castillo",
    "maintainer": "Javier López Castillo",
    'website': "https://nndeveloper.com",

    'category': 'account',
    'version': '0.1',

    'depends': [
        'base',
        'account'
    ],

    'data': [
        'data/data.xml',
        'views/res.users.xml',
        'views/account.journal.xml',
        'views/res.partner.bank.xml',
    ],
    "installable": True,
    "application": True,
    "license": 'LGPL-3',
}
