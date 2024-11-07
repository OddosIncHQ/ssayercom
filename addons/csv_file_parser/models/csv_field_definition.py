from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CSVFieldDefinition(models.Model):
    _name = 'csv.field.definition'
    _description = 'CSV Field Definition'

    # Fields
    field_name = fields.Char(string='CSV Field Name', required=True)
    odoo_field_name = fields.Char(string='Odoo Technical Field Name', required=True)
    mnemonic_name = fields.Char(string='Mnemonic Name', required=False)
    
    field_type = fields.Selection([
        ('char', 'Character'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('boolean', 'Boolean'),
        ('monetary', 'Monetary'),
        ('selection', 'Selection'),
    ], string='Field Type', required=True)

    description = fields.Text(string='Description')

    row_number = fields.Integer(string='Row Number', required=False, default=0, help="Row number where the field is located in the CSV.")
    column_number = fields.Integer(string='Column Number', required=False, default=0, help="Column number where the field is located in the CSV.")

    # For selection fields
    selection_options = fields.Char(string='Selection Options', help="Comma-separated list of options for selection fields.")

    # New 'section' field to categorize fields based on CSV section
    section = fields.Selection([
        ('general', 'General'),
        ('additional', 'Additional'),
        ('form_22', 'Form 22'),
        ('form_50', 'Form 50'),
    ], string='Section', help="Used to categorize fields in the CSV by section.", required=True)

    _sql_constraints = [
        ('unique_odoo_field_name', 'UNIQUE(odoo_field_name)', 'The Odoo technical field name must be unique!'),
    ]

    @api.constrains('odoo_field_name')
    def _check_odoo_field_name(self):
        """
        Ensure that the Odoo technical field name is unique within the model.
        """
        for record in self:
            if self.search_count([('odoo_field_name', '=', record.odoo_field_name), ('id', '!=', record.id)]) > 0:
                raise ValidationError(_("The Odoo technical field name '{}' must be unique.").format(record.odoo_field_name))

    @api.constrains('row_number', 'column_number')
    def _check_positive_values(self):
        """
        Ensure that row_number and column_number are positive integers.
        """
        for record in self:
            if record.row_number < 0:
                raise ValidationError(_("Row number must be a positive integer."))
            if record.column_number < 0:
                raise ValidationError(_("Column number must be a positive integer."))

    @api.model
    def create(self, vals_list):
        """
        Override create to ensure odoo_field_name uniqueness and handle batch creation.
        """
        if isinstance(vals_list, list):
            # Ensure each 'odoo_field_name' is unique before creating batch records.
            for vals in vals_list:
                if 'odoo_field_name' in vals and self.search([('odoo_field_name', '=', vals['odoo_field_name'])]):
                    raise ValidationError(_("The Odoo technical field name '{}' already exists.").format(vals['odoo_field_name']))
            return super(CSVFieldDefinition, self).create(vals_list)
        else:
            # Single record creation
            if 'odoo_field_name' in vals_list and self.search([('odoo_field_name', '=', vals_list['odoo_field_name'])]):
                raise ValidationError(_("The Odoo technical field name '{}' already exists.").format(vals_list['odoo_field_name']))
            return super(CSVFieldDefinition, self).create(vals_list)

    def write(self, vals):
        """
        Override write to ensure odoo_field_name uniqueness on updates.
        """
        if 'odoo_field_name' in vals:
            for record in self:
                if self.search([('odoo_field_name', '=', vals['odoo_field_name']), ('id', '!=', record.id)]):
                    raise ValidationError(_("The Odoo technical field name '{}' already exists.").format(vals['odoo_field_name']))
        return super(CSVFieldDefinition, self).write(vals)
