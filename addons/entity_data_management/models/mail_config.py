from odoo import models, fields, api, _

class MailConfig(models.Model):
    _name = 'mail.config'
    _description = 'Mail Configuration'

    name = fields.Char(string='Name', required=True, default="Mail Configuration")
    imap_server = fields.Char(string='IMAP Server', required=True)
    imap_port = fields.Integer(string='IMAP Port', required=True, default=993)
    username = fields.Char(string='Username', required=True)
    password = fields.Char(string='Password', required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        vals['password'] = self._encrypt_password(vals['password'])
        return super(MailConfig, self).create(vals)

    def write(self, vals):
        if 'password' in vals:
            vals['password'] = self._encrypt_password(vals['password'])
        return super(MailConfig, self).write(vals)

    def _encrypt_password(self, password):
        # Implement encryption logic here, e.g., using Fernet from the cryptography package
        from cryptography.fernet import Fernet
        cipher_suite = Fernet(Fernet.generate_key())
        encrypted_pwd = cipher_suite.encrypt(password.encode())
        return encrypted_pwd.decode()
