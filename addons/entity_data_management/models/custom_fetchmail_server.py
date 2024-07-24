from odoo import models, fields, api, _
from odoo.exceptions import UserError
import imaplib
import email

class CustomFetchmailServer(models.Model):
    _inherit = 'fetchmail.server'

    display_name = fields.Char(string='Display Name', compute='_compute_display_name')
    object_id = fields.Many2one('ir.model', string='Create New Record', ondelete='set null')

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name

    def _fetch_and_process_emails(self):
        config = self.env['mail.config'].search([('active', '=', True)], limit=1)
        if not config:
            return
        
        try:
            mail = imaplib.IMAP4_SSL(config.imap_server, config.imap_port)
            mail.login(config.username, config.password)
            mail.select("inbox")
            
            result, data = mail.search(None, '(UNSEEN)')
            if result == 'OK':
                mail_ids = data[0].split()
                for mail_id in mail_ids:
                    result, message_data = mail.fetch(mail_id, '(RFC822)')
                    if result == 'OK':
                        raw_email = message_data[0][1]
                        email_message = email.message_from_bytes(raw_email)
                        for part in email_message.walk():
                            if part.get_content_maintype() == 'multipart':
                                continue
                            if part.get('Content-Disposition') is None:
                                continue

                            file_name = part.get_filename()
                            if file_name:
                                file_path = f"/mnt/data/{file_name}"
                                with open(file_path, 'wb') as f:
                                    f.write(part.get_payload(decode=True))
                                self.env['entity.data'].process_file(file_path, 'email')

                        mail.store(mail_id, '+FLAGS', '\\Seen')
            mail.logout()
        except Exception as e:
            raise UserError(_('Failed to fetch emails: %s') % str(e))
