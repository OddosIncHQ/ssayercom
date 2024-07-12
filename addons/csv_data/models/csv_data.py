from odoo import models, fields, api
import base64

class CSVData(models.Model):
    _name = 'csv.data'
    _description = 'CSV Data'
    _rec_name = 'x_mojo_rut'

    x_mojo_rut = fields.Char(string='RUT', required=True)
    x_mojo_process_date = fields.Date(string='Process Date', required=True)
    x_mojo_file_code = fields.Char(string='File Code', required=True)
    # Add other predefined fields here

    @api.model
    def import_csv_data(self, csv_content):
        import csv
        from io import StringIO
        
        delimiters = [',', ';', '\t']
        csv_file = StringIO(csv_content)
        
        for delimiter in delimiters:
            csv_file.seek(0)  # Reset file position to the beginning
            reader = csv.reader(csv_file, delimiter=delimiter)
            try:
                headers = next(reader)
                if len(headers) > 1:  # Assuming a valid CSV has more than one column
                    break
            except Exception as e:
                continue
        else:
            raise ValueError("Failed to determine the correct delimiter.")
        
        csv_file.seek(0)
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        
        for row in reader:
            data = {}
            for key, value in row.items():
                field_name = f'x_mojo_{key.lower().replace(" ", "_")}'
                if not hasattr(self, field_name):
                    field_type = self._ask_user_for_field_type(field_name)
                    if field_type:
                        self._create_new_field(field_name, field_type)
                data[field_name] = value
            self.create(data)

    def _ask_user_for_field_type(self, field_name):
        # Simulate prompting the user for field type
        print(f"Field {field_name} does not exist. Please specify the field type.")
        # In actual implementation, replace this with proper UI prompt
        # For example, return 'char' for text fields, 'date' for date fields, etc.
        return 'char'

    def _create_new_field(self, field_name, field_type):
        if field_type == 'char':
            field = fields.Char(string=field_name)
        elif field_type == 'text':
            field = fields.Text(string=field_name)
        elif field_type == 'date':
            field = fields.Date(string=field_name)
        elif field_type == 'int':
            field = fields.Integer(string=field_name)
        elif field_type == 'float':
            field = fields.Float(string=field_name)
        elif field_type == 'bool':
            field = fields.Boolean(string=field_name)
        else:
            return False

        self._add_field(field_name, field)
        return True

    @api.model
    def _add_field(self, field_name, field):
        self._fields[field_name] = field
        self._field_inherits[field_name] = field

class CSVDataFile(models.Model):
    _name = 'csv.data.file'
    _description = 'CSV Data File'
    
    x_mojo_file_code = fields.Char(string='File Code', required=True)
    x_mojo_process_date = fields.Date(string='Process Date', required=True)
    x_mojo_file_content = fields.Binary(string='File Content', required=True)
    x_mojo_csv_data_ids = fields.One2many('csv.data', 'x_mojo_file_code', string='CSV Data')
    
    def import_file(self):
        for record in self:
            csv_content = base64.b64decode(record.x_mojo_file_content).decode('utf-8')
            self.env['csv.data'].import_csv_data(csv_content)
