{
    'name': 'Mojo Customs',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Custom module for managing custom functionalities',
    'description': 'Handles custom functionalities for Mojo System',
    'depends': ['base', 'mail', 'contacts'],  # Add any additional dependencies here
    'data': [
        'views/ir_actions_act_window.xml',
        'views/ir_ui_view.xml',
        'views/ir_model.xml',
        'views/ir_model_access.xml',
        'views/ir_rule.xml',
        'views/res_groups.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
