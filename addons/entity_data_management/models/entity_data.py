from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EntityData(models.Model):
    _name = 'entity.data'
    _description = 'Entity Data'

    name = fields.Char(string='Name', required=True)
    vat = fields.Char(string='VAT', required=True)
    type = fields.Selection([
        ('pn', 'Persona Natural'),
        ('pj', 'Persona Jurídica'),
        ('oth', 'Others'),
    ], string='Type', required=True)
    date_time = fields.Datetime(string='Date and Time of Issue', required=True)
    file_code = fields.Char(string='File Code', required=True)
    file_attachment = fields.Binary(string="File Attachment")
    file_processed = fields.Binary(string="Processed File")
    pdf_form_result = fields.Binary(string="PDF Form Result")
    upload_datetime = fields.Datetime(string='Upload DateTime', default=fields.Datetime.now)
    upload_type = fields.Selection([
        ('type1', 'Type 1'),
        ('type2', 'Type 2')
    ], string='Upload Type', required=True)

    @api.constrains('vat')
    def _check_vat(self):
        if not self.vat or len(self.vat) < 5:
            raise ValidationError(_('VAT must be at least 5 characters long.'))

    @api.model
    def create(self, vals):
        record = super(EntityData, self).create(vals)
        return record
