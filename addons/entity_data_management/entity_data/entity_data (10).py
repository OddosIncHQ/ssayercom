from odoo import models, fields, api

class EntityData(models.Model):
    _name = 'entity.data'
    _description = 'Entity Data'

    name = fields.Char(string='Name')
    rut = fields.Char(string='RUT')  # Field for RUT/RUN
    partner_id = fields.Many2one('res.partner', string='Partner')
    vat = fields.Char(related='partner_id.vat', string='VAT')  # Linked to res.partner.vat
    type = fields.Selection([
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
    ], string='Type')
    date_time = fields.Datetime(string='Date Time')
    file_code = fields.Char(string='File Code')
    upload_datetime = fields.Datetime(string='Upload Date Time')
    upload_type = fields.Selection([
        ('manual', 'Manual'),
        ('auto', 'Automatic'),
    ], string='Upload Type')
    
    description = fields.Text(string='Description')
    file_attachment = fields.Binary(string='File Attachment')
    file_processed = fields.Binary(string="Processed File")
    pdf_form_result = fields.Binary(string="PDF Form Result")
    email_date = fields.Datetime(string='Email Date')
    csv_file_name = fields.Char(string='CSV File Name')
    email_sender = fields.Char(string='Email Sender')
    csv_creation_date = fields.Datetime(string='CSV Creation Date')
    
    _sql_constraints = [
        ('unique_rut_date', 'unique(rut, date_time)', 'The combination of RUT and date must be unique!')
    ]

    @api.model
    def process_csv_data(self, csv_file):
        for row in csv_file:
            rut = row.get('RUT') or row.get('RUN')
            if rut:
                # Check if the partner already exists
                partner = self.env['res.partner'].search([('vat', '=', rut)], limit=1)
                if not partner:
                    # Create a new partner if not found
                    partner = self.env['res.partner'].create({
                        'name': row.get('name'),
                        'vat': rut,
                    })

                # Store the data in the entity data model
                self.create({
                    'name': row.get('name'),
                    'rut': rut,
                    'partner_id': partner.id,
                    'vat': partner.vat,
                    'type': row.get('type'),
                    'date_time': row.get('date_time'),
                    'file_code': row.get('file_code'),
                    'upload_datetime': row.get('upload_datetime'),
                    'upload_type': row.get('upload_type'),
                })
