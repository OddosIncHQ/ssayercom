from odoo import models, fields

class EmailProcessing(models.Model):
    _name = 'email.processing'
    _description = 'Email Processing'

    email_id = fields.Many2one('mail.message', string='Email', required=True)
    processed = fields.Boolean(string='Processed', default=False)
    process_date = fields.Datetime(string='Process Date')
    
    name = fields.Char(string='Name')
    subject = fields.Char(string='Subject')
    sender = fields.Char(string='Sender')
    received_date = fields.Datetime(string='Received Date')
