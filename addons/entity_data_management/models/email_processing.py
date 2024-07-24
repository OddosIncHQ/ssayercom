from odoo import models, fields, api

class EmailProcessing(models.Model):
    _name = 'email.processing'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'email.attachment.handler']
    _description = 'Email Processing'

    name = fields.Char(string='Name')

    @api.model
    def scheduled_email_fetch(self):
        self.env['fetchmail.server']._fetch_and_process_emails()
