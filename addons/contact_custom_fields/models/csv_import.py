import csv
import base64
from odoo import models, fields, api

class ContactCSVImport(models.Model):
    _name = 'contact.csv.import'
    _description = 'Contact CSV Import'

    name = fields.Char(string='Name')
    data = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='File Name')

    @api.model
    def import_csv(self, attachment_id):
        attachment = self.env['ir.attachment'].browse(attachment_id)
        csv_data = base64.b64decode(attachment.datas).decode('utf-8').splitlines()
        reader = csv.DictReader(csv_data)
        
        for row in reader:
            self.env['res.partner'].create({
                'name': row.get('name'),
                'rut_cl': row.get('rut_cl'),
                'sii_pass': row.get('sii_pass'),
                # Añadir otros campos según el contenido del CSV
            })

    @api.model
    def process_csv_attachments(self):
        attachments = self.env['ir.attachment'].search([('res_model', '=', 'contact.csv.import')])
        for attachment in attachments:
            self.import_csv(attachment.id)

