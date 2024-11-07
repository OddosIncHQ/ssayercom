{
    'name': 'CSV File Parser 3.1',
    'version': '3.0',
    'category': 'Tools',
    'summary': 'Automated CSV File Upload, Parsing with Dynamic Cod.XXX Handling and RUT Association',
    'description': """
        The CSV File Parser module allows users to upload, parse, and manage CSV files, with advanced dynamic field handling for forms like Form 22, Form 29, and Declaración Jurada.
    """,
    'author': 'Oddos Solutions LLC',
    'website': 'https://www.oddos.io',
    'license': 'LGPL-3',

    # Dependencies
    'depends': ['base', 'documents', 'mail', 'web'],
    
    # Assets
    'assets': {
        'web.assets_backend': [
            '/csv_file_parser/static/src/js/csv_file_parser_dynamic.js',
            '/csv_file_parser/static/src/xml/csv_file_parser_dynamic_templates.xml',
        ],
        'web.assets_qweb': [
            '/csv_file_parser/static/src/xml/csv_file_parser_dynamic_templates.xml',
        ],
    },
    
    # Data Files
    'data': [
        # Load the tree views first
        'views/view_csv_form22_data_tree.xml',  # Form 22 tree view
        'views/view_csv_form50_data_tree.xml',  # Form 50 tree view

        # Action and Menu Views (load actions after the views are available)
        'views/csv_file_parser_actions.xml',
        'views/csv_rut_manager_actions.xml',
        'views/csv_file_parser_failed_actions.xml',
        'views/menu_items.xml',
        'views/csv_parsed_data_actions.xml',

        # Form and Tree Views
        'views/csv_file_parser_form_views.xml',
        'views/csv_file_parser_tree_views.xml',
        'views/csv_parsed_data_tree_view.xml',
        'views/csv_file_parser_failed_tree_views.xml',
        'views/csv_file_parser_display_table.xml',
        'views/csv_file_parser_analysis_views.xml',

        # Search Views
        'views/csv_parsed_data_search_views.xml',
        'views/csv_file_parser_failed_search_views.xml',

        # CSV Parsing Settings and Configuration
        'views/csv_file_parser_settings_view.xml',
        'data/csv_file_parser_default_settings.xml',

        # Document Inheritance and Form Views
        'views/csv_document_inherit_view.xml',
        'views/csv_file_parser_view.xml',
        'views/rut_manager_views.xml',
        'views/csv_field_definition_views.xml',

        # Security Access Rules
        'security/ir.model.access.csv',

        # Automated Tasks (Cron Jobs) and Mail Configuration
        'data/ir_cron_data.xml',
        'data/mail_alias.xml',
        'data/csv_field_definitions_data.xml',
    ],
    
    # Images
    'images': ['static/description/icon.png'],
    
    # Install Configuration
    'installable': True,
    'application': True,
    'auto_install': False,
}
