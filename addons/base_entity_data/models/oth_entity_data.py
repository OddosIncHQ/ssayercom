from odoo import models, fields

class OthEntityData(models.Model):
    _name = 'oth.entity.data'
    _description = 'Other Entity Data'

    name = fields.Char(string='Name')
    vat = fields.Char(string='VAT')
    type = fields.Selection([
        ('pn', 'Persona Natural'),
        ('pj', 'Persona Jurídica'),
        ('oth', 'Others'),
    ], string='Type')
    date_time = fields.Datetime(string='Date and Time of Issue')
    file_code = fields.Char(string='File Code')
    file_attachment = fields.Binary(string="File Attachment")
    file_processed = fields.Binary(string="Processed File")
    pdf_form_result = fields.Binary(string="PDF Form Result")
    upload_datetime = fields.Datetime(string='Upload DateTime')
    upload_type = fields.Selection([
        ('type1', 'Type 1'),
        ('type2', 'Type 2')
    ], string='Upload Type')
