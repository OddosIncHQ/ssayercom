from odoo import models, fields, api
import imaplib
import email

class CustomFetchmailServer(models.Model):
    _inherit = 'fetchmail.server'

    l10n_cl_is_dte = fields.Boolean(string='DTE')
    l10n_cl_last_uid = fields.Char(string='Last UID')
    display_name = fields.Char(string='Display Name', compute='_compute_display_name')
    object_id = fields.Many2one('ir.model', string='Create New Record', ondelete='set null')

    def _fetch_and_process_emails(self):
        config = self.env['mail.config'].search([('active', '=', True)], limit=1)
        if not config:
            return

        try:
            with imaplib.IMAP4_SSL(config.imap_server, config.imap_port) as mail:
                mail.login(config.username, config.password)
                mail.select("inbox")

                result, data = mail.search(None, '(UNSEEN)')
                mail_ids = data[0].split()

                for mail_id in mail_ids:
                    result, message_data = mail.fetch(mail_id, '(RFC822)')
                    raw_email = message_data[0][1]
                    email_message = email.message_from_bytes(raw_email)

                    for part in email_message.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        file_name = part.get_filename()
                        if file_name:
                            file_data = part.get_payload(decode=True)
                            self.env['ir.attachment'].create({
                                'name': file_name,
                                'datas': file_data,
                                'res_model': 'custom_fetchmail_server',  # Make sure this references your custom model
                                'res_id': self.id,
                            })
        except Exception as e:
            self.env['mail.message'].create({
                'subject': 'Fetchmail Error',
                'body': f'Error while fetching emails: {str(e)}',
                'model': 'custom_fetchmail_server',  # Ensure this references your custom model
                'res_id': self.id,
            })

    def action_retry(self):
        """Additional method to retry processing emails."""
        self._fetch_and_process_emails()
