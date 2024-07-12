{
    'name': 'SoothSayer Module',
    'version': '1.0',
    'summary': 'Module for uploading and storing CSV data from SoothSayer',
    'author': 'Your Name',
    'depends': ['base', 'contacts', 'mojo_customs'],  # Ensure mojo_customs is the correct dependency
    'data': [
    'views/main_model_views.xml',
    'views/form_model_views.xml',
    'views/csv_import_wizard_views.xml',
    'data/data.xml',
],
    'installable': True,
    'application': True,
}
