{
    'name': 'Entity Data Management',
    'version': '17.0.0.1.1',
    'summary': 'Manage entity data from CSV files',
    'license': 'LGPL-3',
    'author': 'Oddos Solutions LLC',
    'maintainer': 'Oddos Solutions LLC',
    'website': 'https://www.ssayer.tech',
    'depends': ['base', 'mail', 'contacts', 'entity.data', 'pj.entity.data', 'pn.entity.data', 'oth.entity.data', 'email.processing'],  # Dependencias necesarias
    'data': [
        'views/view_entity_data_form.xml',        # Vistas de formulario consolidadas
        'views/view_entity_data_tree.xml',        # Vistas de árbol consolidadas
        'views/view_email_processing_tree.xml',   # Vistas relacionadas con email processing
        'views/actions_email_csv_data.xml',       # Acciones relacionadas con CSV de email
        'views/view_email_csv_data_tree.xml',     # Vistas de árbol para email CSV data
        'views/view_entity_file_upload_form.xml', # Vistas de formulario para subida de archivos
        'views/actions_entity_data_management.xml', # Acciones para gestión de datos de entidad
        'views/entity_data_management_action_email_processing.xml', # Acciones de procesamiento de email
        'views/docdocks_menu.xml',                # Menú principal
        'views/mail_config_view.xml',             # Configuración de correo
        'views/scheduled_actions.xml',            # Acciones programadas
        'views/fetchmail_server_views.xml',       # Vistas para fetchmail server
        'views/oth_views.xml',                    # Vistas para otros modelos de entidad
        'security/ir.model.access.csv',           # Seguridad y acceso a modelos
    ],
    'images': [
        'static/src/img/image_80x80.png',
    ],
    'installable': True,
    'application': True,
    'description': """
    Proprietary module developed by Oddos Solutions LLC for SoothSayer Holdings LLC.
    This module is not to be used, modified, or distributed without express permission from SoothSayer Holdings LLC.
    """,
}
