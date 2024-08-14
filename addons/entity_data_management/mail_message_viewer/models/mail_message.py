from odoo import models, fields

class MailMessageViewer(models.Model):
    _name = 'mail.message.viewer'
    _description = 'Mail Message Viewer'

    sender = fields.Char(string='Sender')
    body = fields.Text(string='Body')
    received_date = fields.Datetime(string='Received Date')
