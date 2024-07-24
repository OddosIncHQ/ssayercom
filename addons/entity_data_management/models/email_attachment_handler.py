from odoo import models, api, _
from odoo.exceptions import UserError
import base64
import os

class EmailAttachmentHandler(models.AbstractModel):
    _name = 'email.attachment.handler'
    _inherit = 'mail.thread'
    _description = 'Email Attachment Handler'

    def _extract_attachments(self, mail):
        attachments = self.env['ir.attachment'].search([('res_id', '=', mail.id)])
        for attachment in attachments:
            if 'reporte-' in attachment.name and attachment.name.endswith('.csv'):
                try:
                    file_content = base64.b64decode(attachment.datas)
                    file_path = f"/mnt/data/{attachment.name}"
                    with open(file_path, 'wb') as f:
                        f.write(file_content)
                    self.env['entity.data'].process_file(file_path, 'email')
                except Exception as e:
                    raise UserError(_('Failed to process attachment: %s') % str(e))

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        record = super(EmailAttachmentHandler, self).message_new(msg_dict, custom_values)
        self._extract_attachments(record)
        return record

    @api.model
    def message_update(self, msg_dict, update_vals=None):
        record = super(EmailAttachmentHandler, self).message_update(msg_dict, update_vals)
        self._extract_attachments(record)
        return record
