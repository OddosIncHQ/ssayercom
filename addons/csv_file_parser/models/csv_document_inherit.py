from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CSVDocument(models.Model):
    _inherit = 'documents.document'

    # Field to mark if the document is a CSV file
    is_csv_file = fields.Boolean(string='Is CSV File', default=False)

    # Link to the related CSV File Parser entry
    related_csv_parser_id = fields.Many2one(
        'csv.file.parser', 
        string='Related CSV Parser',
        help="Link to the CSV File Parser that processed this document."
    )
    
    # Optional: Field to display parsing status (if available)
    parsing_status = fields.Selection(
        [('pending', 'Pending'), ('processed', 'Processed'), ('error', 'Error')],
        string='Parsing Status',
        default='pending',
        help="Displays the status of the CSV file parsing process."
    )

    @api.onchange('is_csv_file')
    def _onchange_is_csv_file(self):
        """Handle default actions when a file is marked as a CSV file."""
        if self.is_csv_file:
            self.parsing_status = 'pending'
            # Additional logic can be added here as needed

    @api.constrains('is_csv_file', 'related_csv_parser_id')
    def _check_csv_file_constraints(self):
        """Ensure that CSV files have a related parser and vice versa."""
        for record in self:
            if record.is_csv_file and not record.related_csv_parser_id:
                raise ValidationError(_("CSV files must be linked to a CSV File Parser."))
            if record.related_csv_parser_id and not record.is_csv_file:
                raise ValidationError(_("Documents linked to a CSV File Parser must be marked as CSV files."))

    @api.constrains('parsing_status')
    def _check_valid_parsing_status(self):
        """Ensure the parsing status is valid when marked as CSV."""
        for record in self:
            if record.is_csv_file and not record.parsing_status:
                raise ValidationError(_("A parsing status is required for CSV files."))
