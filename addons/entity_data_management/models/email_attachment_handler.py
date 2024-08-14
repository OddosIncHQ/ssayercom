from odoo import models, fields

class EmailAttachmentHandler(models.Model):
    _name = 'email.attachment.handler'
    _description = 'Email Attachment Handler'

    name = fields.Char(string='Attachment Name', required=True)
    datas = fields.Binary(string='Attachment Data', required=True)
    res_model = fields.Char(string='Related Document Model')
    res_id = fields.Integer(string='Related Document ID')
    upload_datetime = fields.Datetime(string='Upload DateTime')
    upload_type = fields.Selection([
        ('type1', 'FetchMail'),
        ('type2', 'Manual')
    ], string='Upload Type')
