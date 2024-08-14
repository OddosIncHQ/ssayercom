from odoo.tests.common import TransactionCase

class TestEntityDataManagement(TransactionCase):
    def test_model_fields(self):
        # Create a record and test the fields
        entity = self.env['entity.data'].create({
            'name': 'Test Entity',
            'vat': '1234567890',
            'type': 'example',
            'date_time': '2024-01-01 00:00:00',
            'file_code': 'TEST001',
            'upload_type': 'manual'
        })
        self.assertEqual(entity.name, 'Test Entity')
        self.assertEqual(entity.vat, '1234567890')

    def test_views(self):
        # Test the views by loading them and checking the field existence
        view = self.env.ref('entity_data_management.view_entity_data_form')
        self.assertIn('name', view.arch_db)
        self.assertIn('vat', view.arch_db)
