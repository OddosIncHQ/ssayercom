from odoo import models, fields

class MailConfig(models.Model):
    _name = 'mail.config'
    _description = 'Mail Configuration'

    imap_server = fields.Char(string='IMAP Server', required=True)
    imap_port = fields.Integer(string='IMAP Port', required=True)
    username = fields.Char(string='Username', required=True)
    password = fields.Char(string='Password', required=True)
    active = fields.Boolean(string='Active', default=True)
