from odoo import models, fields, api

class EmailProcessing(models.Model):
    _name = 'email.processing'
    _description = 'Email Processing Model'

    name = fields.Char(string='Name', required=True)
    email_id = fields.Many2one('mail.message', string='Email', required=True)
    processed = fields.Boolean(string='Processed', default=False)
    process_date = fields.Datetime(string='Process Date')
