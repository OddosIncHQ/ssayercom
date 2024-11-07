from odoo import http
from odoo.http import request
import base64
import logging
import re
import json
from datetime import datetime

_logger = logging.getLogger(__name__)

class CSVFileParserController(http.Controller):

    @http.route('/csv_file_parser/upload', type='http', auth='user', methods=['POST'], csrf=True)
    def upload_csv(self, **post):
        """
        This route handles CSV file uploads via POST requests.
        It processes the file and stores it in the Documents module.
        """
        # Get the file and other information from the request
        csv_file = post.get('csv_file')
        file_name = post.get('file_name')
        upload_type = post.get('upload_type', 'M')  # Default to "M" for manual upload

        if not csv_file or not file_name:
            _logger.error("No file or file name provided")
            return request.make_response(json.dumps({
                "status": "error",
                "message": "No file or file name provided"
            }), headers=[('Content-Type', 'application/json')], status=400)

        # Validate file type (must be CSV)
        if not file_name.endswith('.csv'):
            _logger.error(f"Invalid file type: {file_name}")
            return request.make_response(json.dumps({
                "status": "error",
                "message": "Invalid file type. Only CSV files are allowed."
            }), headers=[('Content-Type', 'application/json')], status=400)

        try:
            # Convert the file to binary data (expected by Odoo)
            file_data = base64.b64encode(csv_file.read())

            # Dynamically fetch folder ID (or use default 15 if not set)
            folder_id = request.env['ir.config_parameter'].sudo().get_param('csv_file_parser.default_folder_id', 15)

            # Ensure the folder exists (create if necessary)
            folder = request.env['documents.folder'].sudo().browse(int(folder_id))
            if not folder.exists():
                _logger.info(f"Folder ID {folder_id} not found, creating new folder for CSV files")
                folder = request.env['documents.folder'].sudo().create({
                    'name': 'CSV Files',
                    'parent_folder_id': None,
                })
                folder_id = folder.id

            # Determine RUT and creation date for file naming
            rut_value, creation_date_str = self._get_rut_and_creation_date(csv_file, file_name)
            
            if not rut_value:
                _logger.error("RUT value could not be extracted from the CSV file or file name.")
                return request.make_response(json.dumps({
                    "status": "error",
                    "message": "RUT value could not be extracted from the CSV file or file name."
                }), headers=[('Content-Type', 'application/json')], status=400)

            # Find or create the RUT in 'csv.rut.manager'
            rut = request.env['csv.rut.manager'].sudo().search([('name', '=', rut_value)], limit=1)
            if not rut:
                rut = request.env['csv.rut.manager'].sudo().create({'name': rut_value})

            # Generate the final file name
            final_file_name = self._generate_file_name(rut_value, creation_date_str, file_name, upload_type)

            # Create the CSV File Parser record
            csv_parser_record = request.env['csv.file.parser'].sudo().create({
                'name': final_file_name,
                'file_name': final_file_name,
                'csv_file': file_data,  # Binary-encoded file data
                'rut_id': rut.id,  # Link to the RUT
                'parsing_marker': ',',  # You can pass this dynamically if needed
                'progress_status': 'draft',
            })

            # Store the file in the Documents module
            request.env['documents.document'].create({
                'name': final_file_name,
                'datas': file_data,  # Binary-encoded file data
                'datas_fname': final_file_name,
                'folder_id': folder_id,  # Dynamic folder ID
                'res_model': 'csv.file.parser',
                'res_id': csv_parser_record.id,  # Link to the parser record
                'mimetype': 'text/csv',
            })

            _logger.info(f"CSV file '{final_file_name}' uploaded successfully into folder {folder_id}")

        except Exception as e:
            _logger.error(f"Error during CSV upload: {str(e)}")
            return request.make_response(json.dumps({
                "status": "error",
                "message": f"Error during upload: {str(e)}"
            }), headers=[('Content-Type', 'application/json')], status=500)

        return request.make_response(json.dumps({
            "status": "success",
            "message": "CSV file uploaded successfully"
        }), headers=[('Content-Type', 'application/json')], status=200)

    @http.route('/csv_parser/display_table', type='http', auth='user', website=True)
    def display_table(self, form_name):
        """
        A route to display the table for any form (e.g., 'Formulario 22')
        """
        # Fetch an instance of the CSV parser model (assuming one exists)
        parser = request.env['csv.file.parser'].search([], limit=1)
        
        if not parser:
            return request.not_found()

        # Call the method to generate the table and convert to HTML
        table_html = parser.display_table_with_periods(form_name)
        
        # Render the table in the view template
        return request.render('csv_file_parser.display_table_template', {
            'table_html': table_html,
            'form_name': form_name
        })

    def _get_rut_and_creation_date(self, csv_file, file_name):
        """
        Extract RUT and file creation date from the CSV file content if available.
        """
        try:
            file_content = base64.b64decode(csv_file.read()).decode('utf-8')
            csv_lines = file_content.splitlines()
            rut_value = None
            creation_date_str = None

            # Assuming the first row contains the RUT and optional date
            for idx, row in enumerate(csv_lines):
                if idx == 0:  # First row, try to extract RUT
                    row_data = row.split(',')
                    if len(row_data) > 1:
                        rut_value = row_data[1].replace('-', '')  # Assuming RUT is the second value and remove hyphens
                    break

            # Fallback to file name parsing for the RUT (if not found in the content)
            if not rut_value:
                rut_match = re.search(r'reporte-(.*?)-', file_name)
                if rut_match:
                    rut_value = rut_match.group(1)
                else:
                    _logger.error("RUT value could not be extracted from file name")
                    return None, None

            # Try to get creation date (if available in the file metadata)
            creation_date_str = self._extract_creation_date_from_file_metadata(file_content)
            if not creation_date_str:
                # If no creation date, extract from the file name
                creation_date_match = re.search(r'reporte-(\d{14})', file_name)
                if creation_date_match:
                    creation_date_str = creation_date_match.group(1)
                else:
                    _logger.error("Creation date could not be extracted from file name")
                    return rut_value, None

            return rut_value, creation_date_str

        except Exception as e:
            _logger.error(f"Error extracting RUT and creation date: {str(e)}")
            return None, None

    def _generate_file_name(self, rut_value, creation_date_str, file_name, upload_type):
        """
        Generate the file name based on the RUT, creation date, and upload type (manual/fetched).
        """
        if creation_date_str:
            return f"{rut_value}-{creation_date_str}-{upload_type}"
        else:
            # Fallback: extract text between "reporte-" and ".csv"
            report_match = re.search(r'reporte-(.*?)\.csv', file_name)
            if report_match:
                report_id = report_match.group(1)
                return f"{rut_value}-{report_id}-{upload_type}"
            else:
                return f"{rut_value}-default-{upload_type}"

    def _extract_creation_date_from_file_metadata(self, file_content):
        """
        Extract creation date from file metadata if available.
        This is a placeholder. Adapt it based on the file's actual metadata format.
        """
        # Here you would implement logic to parse the file's metadata and extract the creation date
        # This is often dependent on the specific format of the CSV or related systems
        # For now, return None as a placeholder
        return None

    @http.route('/csv_file_parser/api/get_files', type='json', auth='user', methods=['GET'], csrf=False)
    def get_csv_files(self):
        """
        This route returns a list of all CSV files stored in the Documents module.
        """
        try:
            documents = request.env['documents.document'].search([('mimetype', '=', 'text/csv')])
            _logger.info(f"Retrieved {len(documents)} CSV files from the Documents module")
            return [{'id': doc.id, 'name': doc.name} for doc in documents]
        except Exception as e:
            _logger.error(f"Error fetching CSV files: {str(e)}")
            return request.make_response(json.dumps({
                'status': 'error',
                'message': str(e)
            }), headers=[('Content-Type', 'application/json')], status=500)
