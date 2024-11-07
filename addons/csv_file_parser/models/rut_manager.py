from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RUTManager(models.Model):
    _name = 'csv.rut.manager'
    _description = 'RUT Manager'

    name = fields.Char(string='RUT', required=True, index=True)  # Index for faster searching
    description = fields.Text(string='Description')
    contribuyente_type = fields.Char(string="Contribuyente Type")  # Persona Jurídica, etc.
    company_type = fields.Char(string="Company Type")  # MICRO EMPRESA, etc.
    business_activity = fields.Char(string="Business Activity")  # Business activities description
    activity_code = fields.Char(string="Activity Codes")  # The activity codes, like 702000, 643000
    office_address = fields.Text(string="Office Address")  # Office address for in-person formalities
    form_submission_data = fields.Text(string="Form Submission Data")  # Store the forms and submission details as text or JSON

    parser_ids = fields.One2many('csv.file.parser', 'rut_id', string='Parsed Files')
    parser_count = fields.Integer(string='CSV File Count', compute='_compute_parser_count', store=True)  # Store computed value

    _sql_constraints = [
        ('rut_unique', 'unique (name)', 'The RUT must be unique!'),
    ]

    @api.depends('parser_ids')
    def _compute_parser_count(self):
        """Compute the count of CSV File Parsers associated with this RUT."""
        for record in self:
            record.parser_count = len(record.parser_ids)

    @api.constrains('name')
    def _check_unique_rut(self):
        """Ensure that the RUT is unique."""
        for record in self:
            if self.search([('name', '=', record.name), ('id', '!=', record.id)]):
                raise ValidationError(_("The RUT '{}' already exists and must be unique.").format(record.name))

    @api.model
    def create(self, vals_list):
        """Override create to handle batch creation and ensure RUT uniqueness."""
        # Check if we're handling multiple records (batch creation)
        if isinstance(vals_list, list):
            # Ensure each RUT is unique before batch creation
            for vals in vals_list:
                if 'name' in vals and self.search([('name', '=', vals['name'])]):
                    raise ValidationError(_("The RUT '{}' already exists.").format(vals['name']))
            # Batch create records
            records = super(RUTManager, self).create(vals_list)
        else:
            # Single record creation
            if 'name' in vals_list and self.search([('name', '=', vals_list['name'])]):
                raise ValidationError(_("The RUT '{}' already exists.").format(vals_list['name']))
            records = super(RUTManager, self).create([vals_list])
        
        return records

    def write(self, vals):
        """Override write to ensure the RUT uniqueness on updates."""
        if 'name' in vals:
            for record in self:
                if self.search([('name', '=', vals['name']), ('id', '!=', record.id)]):
                    raise ValidationError(_("The RUT '{}' already exists.").format(vals['name']))
        return super(RUTManager, self).write(vals)
