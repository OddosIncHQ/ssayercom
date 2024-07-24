{
    'name': 'Entity Data Management',
    'version': '17.0.0.0.1',
    'summary': 'Manage entity data from CSV files',
    'license': 'Other proprietary',
    'author': 'SootHsayer Holdings LLC',
    'maintainer': 'Oddos Solutions LLC',
    'website': 'https://www.ssayyer.tech',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/entity_file_upload.xml',
        'views/entity_file_report.xml',
        'views/entity_data.xml',
        'views/mail_config_view.xml',
        'data/scheduled_actions.xml',
        'views/docdocks_menu.xml',
        'views/fetchmail_server_views.xml'
    ],
    'images': ['static/description/image_80x80.png'],
    'installable': True,
    'application': True,
    'description': """
        Proprietary module developed by Oddos Solutions LLC for SootHsayer Holdings LLC.
        This module is not to be used, modified, or distributed without express permission from SootHsayer Holdings LLC.
    """,
}
