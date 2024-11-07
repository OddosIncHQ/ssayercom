from odoo import models, fields, api, _
from datetime import datetime  # Add this line
import base64
import io
import csv
import re
import logging
from odoo.exceptions import ValidationError
import pandas as pd  # To use for table generation


_logger = logging.getLogger(__name__)

class CSVFileParser(models.Model):
    _name = 'csv.file.parser'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'CSV File Parser'

    # Fields
    name = fields.Char(string='File Name')
    file_name = fields.Char(string='Uploaded File Name')
    csv_file = fields.Binary(string='CSV File', required=False)
    parsed_data_ids = fields.One2many('csv.parsed.data', 'parser_id', string='Parsed Data')
    rut_id = fields.Many2one('csv.rut.manager', string='RUT')
    parsing_result = fields.Text(string="Parsing Result", readonly=True)
    alias_model_id = fields.Many2one('ir.model', string="Alias Model", help="Optional alias for models.")
    parsing_marker = fields.Char(string="Parsing Marker", default=',', help="Marker used to parse CSV files.")
    alias_id = fields.Many2one('mail.alias', string="Alias", ondelete="restrict", help="Email alias linked to this parser, used to fetch incoming emails with attached CSVs.")
    progress_status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('error', 'Error')
    ], string="Progress Status", default='draft', readonly=True, help="Tracks the progress of the CSV file parsing.")
    log_details = fields.Text(string='Log Details', readonly=True, help="Detailed logs of the CSV parsing process.")
    error_traceback = fields.Text(string='Error Traceback', readonly=True, help="Traceback details for any errors encountered during parsing.")
    related_document_id = fields.Many2one('ir.attachment', string="Related Document", help="The related document for this CSV parser record.")
    creation_date = fields.Date(string='File Creation Date', readonly=True)

    additional_data_ids = fields.One2many('csv.additional.data', 'parser_id', string='Additional Parsed Data')
    form_22_data_ids = fields.One2many('csv.form22.data', 'parser_id', string='Form 22 Data')
    form_50_data_ids = fields.One2many('csv.form50.data', 'parser_id', string='Form 50 Data')

    @api.onchange('csv_file')
    def _onchange_csv_file(self):
        """Process the CSV file when uploaded manually and check for file duplicity."""
        if self.csv_file:
            # Check for file duplicity
            existing_file = self.env['ir.attachment'].search([('name', '=', self.file_name)], limit=1)
            if existing_file:
                raise ValidationError(_('A file with this name already exists.'))

            try:
                # Decode CSV file (attempt UTF-8, fallback to Latin-1)
                csv_data = base64.b64decode(self.csv_file)
                try:
                    data_stream = io.StringIO(csv_data.decode('utf-8'))
                except UnicodeDecodeError:
                    _logger.warning(f"UTF-8 decoding failed for file '{self.file_name}', using Latin-1 encoding.")
                    data_stream = io.StringIO(csv_data.decode('latin-1'))

                # Parse RUT from the first row
                csv_reader = csv.reader(data_stream)
                rut_value = next(csv_reader)[1] if csv_reader else None

                if rut_value:
                    rut = self.env['csv.rut.manager'].search([('name', '=', rut_value)], limit=1)
                    if not rut:
                        rut = self.env['csv.rut.manager'].create({'name': rut_value})
                    self.rut_id = rut  # Assign the full record

            except Exception as e:
                _logger.error(f"Error processing CSV file: {str(e)}")
                self.progress_status = 'error'


            # Generate file name if not set
            if not self.file_name:
                vals = {'rut_id': self.rut_id.id if self.rut_id else False, 'csv_file': self.csv_file}
                self.file_name = self.generate_file_name(vals)

    def parse_csv_file(self):
        """Parses the CSV file and updates the status based on success or failure."""
        if not self.csv_file:
            self.parsing_result = _("No CSV file uploaded.")
            _logger.warning(f"No CSV file uploaded for {self.name}")
            return False

        try:
            self.progress_status = 'in_progress'
            
            # Decode CSV file
            csv_data = base64.b64decode(self.csv_file)
            csv_data_io = io.StringIO(csv_data.decode('utf-8'))
            reader = csv.reader(csv_data_io, delimiter=self.parsing_marker, quotechar='"')

            # Read all CSV rows into memory
            raw_data = list(reader)

            # Check if data is empty
            if not raw_data:
                self.parsing_result = _("CSV file is empty.")
                _logger.error(f"CSV file '{self.file_name}' is empty.")
                self.progress_status = 'error'
                return False

            # Clear existing parsed data
            self.parsed_data_ids.unlink()
            self.additional_data_ids.unlink()
            self.form_22_data_ids.unlink()
            self.form_50_data_ids.unlink()

            # Get all dynamic field definitions from csv.field.definition model
            field_definitions = self.env['csv.field.definition'].search([])

            # Process each field definition dynamically
            for field_def in field_definitions:
                row_number = field_def.row_number - 1
                column_number = field_def.column_number - 1

                # Ensure row and column exist in CSV
                if 0 <= row_number < len(raw_data) and 0 <= column_number < len(raw_data[row_number]):
                    value = raw_data[row_number][column_number]
                    odoo_field = field_def.odoo_field_name
                    field_type = field_def.field_type

                    # Convert field based on type
                    if field_type == 'date':
                        value = self.convert_to_date(value)
                    elif field_type in ['float', 'monetary']:
                        value = self.convert_to_float(value)
                    elif field_type == 'boolean':
                        value = self.convert_to_boolean(value)
                    elif field_type == 'selection' and value not in field_def.selection_options.split(','):
                        _logger.warning(f"Invalid selection value '{value}' for field '{odoo_field}'")
                        continue

                    # Store the parsed data
                    if field_def.section == 'general':
                        self.env['csv.parsed.data'].create({
                            'parser_id': self.id,
                            'field_name': odoo_field,
                            'field_value': value,
                        })
                    elif field_def.section == 'additional':
                        self.env['csv.additional.data'].create({
                            'parser_id': self.id,
                            'column_name': odoo_field,
                            'column_value': value,
                        })
                    elif field_def.section == 'form_22':
                        self.env['csv.form22.data'].create({
                            'parser_id': self.id,
                            'code': odoo_field,
                            'value': value,
                        })
                    elif field_def.section == 'form_50':
                        self.env['csv.form50.data'].create({
                            'parser_id': self.id,
                            'code': odoo_field,
                            'value': value,
                        })
                else:
                    _logger.warning(f"Row {field_def.row_number} or Column {field_def.column_number} is out of bounds in file '{self.file_name}'")

            self.progress_status = 'done'
            self.parsing_result = _("CSV file '{}' parsed successfully.").format(self.file_name)
            _logger.info(f"CSV file '{self.file_name}' parsed successfully for {self.name}")

        except Exception as e:
            _logger.error(f"Failed to parse CSV file '{self.file_name}': {str(e)}")
            self.parsing_result = _("Failed to parse CSV file: {}").format(str(e))
            self.log_details = str(e)
            self.error_traceback = str(e)
            self.progress_status = 'error'
            return False

        return True

    def display_table_with_periods(self, form_name):
        """
        Display a table for any form (like Formulario 22 or Declaración Jurada)
        where periods are shown as columns and dynamic fields (e.g., Cod.XXX) are displayed as rows.
        """
        # Fetch the parsed data associated with this form
        parsed_data = self.parsed_data_ids.filtered(lambda d: form_name in d.form_section)

        # Step 1: Extract periods
        periods = [rec.period for rec in parsed_data]

        # Step 2: Extract Cod. fields and their values
        cod_data_rows = []
        for rec in parsed_data:
            for cod_field in rec.cod_fields:
                cod_data_rows.append({
                    'cod_field': cod_field.cod_name,
                    'values': cod_field.cod_value.split(',')  # Assuming values are stored as comma-separated
                })

        # Step 3: Organize the data into a DataFrame
        cod_df_dict = {}
        for cod_row in cod_data_rows:
            values = cod_row['values']
            cod_df_dict[cod_row['cod_field']] = values

        cod_df = pd.DataFrame(cod_df_dict, index=periods).T.reset_index()
        cod_df.rename(columns={'index': 'Cod. Field'}, inplace=True)

        # Return the DataFrame as HTML (for rendering in the view)
        return cod_df.to_html(classes='table table-bordered')

        
    def create(self, vals_list):
        """Override the create method to handle batch creation and generate file names."""
        records = None  # Initialize records to avoid UnboundLocalError

        if isinstance(vals_list, list):  # Batch creation
            for vals in vals_list:
                # Ensure file_name is generated if not provided
                if 'file_name' not in vals:
                    vals['file_name'] = self.generate_file_name(vals)
                vals['creation_date'] = datetime.now().strftime('%Y-%m-%d')

            records = super(CSVFileParser, self).create(vals_list)

            # Save CSV to documents for each record
            for record in records:
                if record.csv_file and record.file_name:
                    self.env['ir.attachment'].create({
                        'name': record.file_name,
                        'datas': record.csv_file,  # Base64-encoded CSV content
                        'res_model': 'csv.file.parser',
                        'res_id': record.id,
                        'type': 'binary',
                        'mimetype': 'text/csv'
                    })
        else:  # Single record creation
            vals_list['creation_date'] = datetime.now().strftime('%Y-%m-%d')
            if 'file_name' not in vals_list:
                vals_list['file_name'] = self.generate_file_name(vals_list)

            records = super(CSVFileParser, self).create([vals_list])

            # Save the CSV to documents for the single record
            if records.csv_file and records.file_name:
                self.env['ir.attachment'].create({
                    'name': records.file_name,
                    'datas': records.csv_file,  # Base64-encoded CSV content
                    'res_model': 'csv.file.parser',
                    'res_id': records.id,
                    'type': 'binary',
                    'mimetype': 'text/csv'
                })

        return records

    def generate_file_name(self, vals):
        """Helper function to generate the file name based on RUT and creation date."""
        rut_value = vals.get('rut_id', 'default_rut')
        creation_date_str = self._extract_creation_date() or self._fallback_file_name()
        upload_type = 'M'
        return f"{rut_value}-{creation_date_str}-{upload_type}"

    def _extract_creation_date(self):
        """Extract creation date from CSV content (if available)."""
        try:
            if not self.csv_file:
                _logger.error("CSV file is not valid for decoding.")
                return None

            csv_data = base64.b64decode(self.csv_file)
            data_stream = io.StringIO(csv_data.decode('utf-8'))

            csv_reader = csv.reader(data_stream)
            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    creation_date_str = row[2]  # Assumes creation date is in the third column
                    if re.match(r'^\d{8}\d{6}$', creation_date_str):  # YYYYMMDDHHMMSS format
                        return creation_date_str
            return None

        except Exception as e:
            _logger.error(f"Error extracting creation date: {str(e)}")
            return None

    def _fallback_file_name(self):
        """Fallback to extracting text between 'reporte-' and '.csv'."""
        attachment = self.env['ir.attachment'].search([('res_model', '=', 'csv.file.parser'), ('res_id', '=', self.id)], limit=1)
        if attachment and attachment.datas_fname:
            report_match = re.search(r'reporte-(.*?)\.csv', attachment.datas_fname)
            if report_match:
                return report_match.group(1)
        return "default_uploaded"

        """Normalize the period format."""
        return period.strip()

    def validate_matrix_size(self, expected_size, parsed_size):
        """Validate that the parsed matrix size matches the expected size."""
        expected_rows, expected_columns = expected_size
        parsed_rows, parsed_columns = parsed_size
        if parsed_rows != expected_rows or parsed_columns != expected_columns:
            _logger.warning(f"Matrix size mismatch: expected {expected_size}, but got {parsed_size}.")

    def extract_matrix_title_and_size(self, row):
        """Extract matrix title and size from a row if it exists."""
        matrix_title_pattern = r'(.+)\((\d+)x(\d+)\)'
        match = re.match(matrix_title_pattern, row[0])
        if match:
            title = match.group(1).strip()
            rows = int(match.group(2))
            columns = int(match.group(3))
            return title, (rows, columns)
        return None, None

    def process_table_row(self, title, columns):
        """Process a data row under a specific table title, handling one-column tables."""
        is_table = len(columns) > 2  # Simple heuristic: if there are many columns, treat it as a table
    
        if len(columns) == 2:  # Handle the one-column case separately
            for idx, value in enumerate(columns[1:], start=1):
                self.env['csv.parsed.data'].create({
                    'parser_id': self.id,
                    'form_section': title,
                    'field_name': f"{title} {columns[0]} Period {idx}",
                    'field_value': value,
                    'type': 'detailed' if is_table else 'general',
                    'is_table': True,
                })
        else:
            for idx, value in enumerate(columns[1:], start=1):
                self.env['csv.parsed.data'].create({
                    'parser_id': self.id,
                    'form_section': title,
                    'field_name': f"{title} {columns[0]} Period {idx}",
                    'field_value': value,
                    'type': 'general' if not is_table else 'detailed',
                    'is_table': is_table,
                })

    def process_declaracion_jurada_subsections(self, parsed_data, start_idx, current_sub_title):
        """Process complex structure for Declaración Jurada sections, including sub-titles."""
        headers = parsed_data[start_idx]

        for col_idx in range(1, len(headers)):  # Start from the second column (skip the title column)
            period = self.normalize_period(headers[col_idx])

            for sub_idx in range(1, len(parsed_data[start_idx:])):  # Start processing rows after header
                sub_row = parsed_data[start_idx + sub_idx]
                if sub_row[0]:
                    self.env['csv.parsed.data'].create({
                        'parser_id': self.id,
                        'form_section': f"{current_sub_title} - Declaración Jurada 1907",
                        'field_name': f"{sub_row[0]} - {period}",
                        'field_value': sub_row[col_idx],
                        'type': 'detailed',
                    })

    def is_sub_title(self, text):
        """Check if a row is a sub-title."""
        known_sub_titles = ["CUADRO RESUMEN FINAL", "B: DATOS DE LOS INFORMADOS", "C: INFORMACIÓN ESPECÍFICA"]
        return any(sub_title in text for sub_title in known_sub_titles)

    def is_table_title(self, text):
        """Check if a text is a table title by matching known patterns."""
        known_titles = [
            "Formularios Presentados", "Anotaciones Vigentes", "Notificaciones",
            "Cartas y correos informativos", "Visitas del SII a sus locales", 
            "Contribuciones territoriales", "Propiedades", "Peticiones Administrativas", 
            "RAV/RAF y Recurso Jerárquico", "Lista Formularios 3280", 
            "Lista Formularios 3600", "Formulario 22", "Formulario 29", "Formulario 50", 
            "Declaraciones Juradas Pendientes", "Declaración Jurada 1907", "Declaración Jurada 1913"
        ]
        return any(title in text for title in known_titles)


class ParsedDataModel(models.Model):
    _name = 'csv.parsed.data'
    _description = 'Parsed Data Model'

    parser_id = fields.Many2one('csv.file.parser', string='CSV Parser', ondelete='cascade')
    field_name = fields.Char(string='Field Name', required=True)
    field_value = fields.Char(string='Field Value', required=True)


class AdditionalDataModel(models.Model):
    _name = 'csv.additional.data'
    _description = 'Additional Data Model'

    parser_id = fields.Many2one('csv.file.parser', string='CSV Parser', ondelete='cascade')
    column_name = fields.Char(string='Column Name', required=True)
    column_value = fields.Char(string='Column Value', required=True)

class Form22DataModel(models.Model):
    _name = 'csv.form22.data'
    _description = 'Form 22 Data Model'

    parser_id = fields.Many2one('csv.file.parser', string='CSV Parser', ondelete='cascade')
    code = fields.Char(string='Code', required=True)
    value = fields.Char(string='Value', required=True)

  
class Form50DataModel(models.Model):
    _name = 'csv.form50.data'
    _description = 'Form 50 Data Model'

    parser_id = fields.Many2one('csv.file.parser', string='CSV Parser', ondelete='cascade')
    code = fields.Char(string='Code', required=True)
    value = fields.Char(string='Value', required=True)
