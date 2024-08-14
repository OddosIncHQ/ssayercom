from odoo import models, fields

class EntityFileUpload(models.Model):
    _name = 'entity.file.upload'
    _description = 'Entity File Upload'

    name = fields.Char(string='Name', required=True)
    file = fields.Binary(string='File', required=True)
    upload_datetime = fields.Datetime(string='Upload DateTime')
    upload_type = fields.Selection([
        ('type1', 'FetchMail'),
        ('type2', 'Manual')
    ], string='Upload Type')

    # Añadir el campo filename
    filename = fields.Char(string='Filename', help="Name of the uploaded file")
