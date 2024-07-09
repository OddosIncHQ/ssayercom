{
    'name': 'SII Data Import',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Importar datos del SII y relacionarlos con contactos',
    'description': """
        Este módulo permite importar datos de archivos CSV del SII y 
        relacionarlos con el módulo de contactos (res.partner).
    """,
    'author': 'Oddos Solutions LLC',
    'depends': ['base', 'contacts'],
    'data': [
        'views/sii_data_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
