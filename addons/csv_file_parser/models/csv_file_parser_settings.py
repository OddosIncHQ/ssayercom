import re  # Add this import at the top of the file
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CSVFileParserSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'CSV File Parser Settings'

    auto_parse = fields.Boolean(string='Auto Parse CSV Files', default=False)
    storage_workspace_id = fields.Many2one('documents.folder', string='Default Storage Workspace')

    alias = fields.Char(string='Mail Alias', help='Specify the alias used for parsing emails.')
    markers = fields.Char(string='Parsing Markers', help='Specify the delimiter used for CSV parsing (e.g., comma or semicolon).')

    max_rows = fields.Integer(string="Max Rows", help="Specify the maximum number of rows to parse from the CSV file.")
    max_columns = fields.Integer(string="Max Columns", help="Specify the maximum number of columns to parse from the CSV file.")

    @api.model
    def get_values(self):
        res = super(CSVFileParserSettings, self).get_values()
        # Fetching config values
        storage_workspace_id = self.env['ir.config_parameter'].sudo().get_param('csv_file_parser.storage_workspace_id', default=0)
    
        # Convert storage_workspace_id from ID to recordset
        storage_workspace = self.env['documents.folder'].browse(int(storage_workspace_id)) if storage_workspace_id else False
    
        res.update(
            auto_parse=self.env['ir.config_parameter'].sudo().get_param('csv_file_parser.auto_parse', default=False),
            storage_workspace_id=storage_workspace,  # Pass the recordset
            alias=self.env['ir.config_parameter'].sudo().get_param('csv_file_parser.alias', default='file-csv-cl@sstechs.io'),
            markers=self.env['ir.config_parameter'].sudo().get_param('csv_file_parser.markers', default=','),
            max_rows=int(self.env['ir.config_parameter'].sudo().get_param('csv_file_parser.max_rows', default=0)),
            max_columns=int(self.env['ir.config_parameter'].sudo().get_param('csv_file_parser.max_columns', default=0)),
        )
        return res

    def set_values(self):
        super(CSVFileParserSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('csv_file_parser.auto_parse', self.auto_parse)
        self.env['ir.config_parameter'].sudo().set_param('csv_file_parser.storage_workspace_id', self.storage_workspace_id.id if self.storage_workspace_id else 0)
        self.env['ir.config_parameter'].sudo().set_param('csv_file_parser.alias', self.alias)
        self.env['ir.config_parameter'].sudo().set_param('csv_file_parser.markers', self.markers)
        self.env['ir.config_parameter'].sudo().set_param('csv_file_parser.max_rows', self.max_rows)
        self.env['ir.config_parameter'].sudo().set_param('csv_file_parser.max_columns', self.max_columns)

    @api.constrains('alias')
    def _check_alias(self):
        """Ensure the alias format is valid."""
        for record in self:
            if record.alias and not re.match(r'^[^@]+@[^@]+\.[^@]+$', record.alias):
                raise ValidationError(_("Please provide a valid email address for the Mail Alias."))

    @api.constrains('max_rows', 'max_columns')
    def _check_positive_values(self):
        """Ensure that max_rows and max_columns are positive integers."""
        for record in self:
            if record.max_rows < 0 or record.max_columns < 0:
                raise ValidationError(_("Max Rows and Max Columns must be non-negative values."))
