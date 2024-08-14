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
        'views/view_entity_data_form.xml',     
        'views/view_entity_data_tree.xml', 
        'email_processing/views/email_processing_view.xml', 
        'email_processing/views/view_email_processing_tree.xml',  # Updated path
        'views/actions_email_csv_data.xml',    
        'views/view_email_csv_data_tree.xml',    
        'views/view_entity_file_upload_form.xml',
        'views/actions_entity_data_management.xml',
        'views/entity_data_management_action_email_processing.xml',  
        'views/docdocks_menu.xml',               
        'views/mail_config_view.xml',            
        'views/scheduled_actions.xml',           
        'views/fetchmail_server_views.xml',      
        'views/oth_views.xml',                    
        'security/ir.model.access.csv',          
    ],

    'images': [
        'static/src/img/image_80x80.png',
    ],
    'demo': [
        'demo/reporte-668ca85844238cbe47789296.csv',
        'demo/reporte-668c01d844238cbe4778926c.csv',
        'demo/reporte-6696d6ad44238cbe477892ec.csv',
        'demo/reporte-6699d96444238cbe47789301.csv',
        'demo/reporte-6699dad244238cbe47789305.csv',
    ],
'installable': True,
    'application': True,
    'description': """
    Proprietary module developed by Oddos Solutions LLC for SoothSayer Holdings LLC.
    This module is not to be used, modified, or distributed without express permission from SoothSayer Holdings LLC.
    """,
}
