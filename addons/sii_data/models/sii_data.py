import csv
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class SiiData(models.Model):
    _name = 'sii.data'
    _description = 'Datos extraídos del SII'

    partner_id = fields.Many2one('res.partner', string='Contacto', ondelete='cascade')
    tipo_contribuyente = fields.Char(string='Tipo de Contribuyente')
    tipo = fields.Char(string='Tipo')
    giro_informado = fields.Char(string='Giro Informado')
    codigo_actividad_informado = fields.Char(string='Código de Actividad Informado')
    oficina_tramites = fields.Char(string='Oficina para Trámites Presenciales')

    @api.model
    def import_csv(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = list(reader)

                if not data:
                    _logger.error("CSV file is empty.")
                    return
                
                partner = None
                for i, line in enumerate(data):
                    if i == 0:  # Assuming the first line contains VAT
                        vat = line[1].strip()
                        partner = self.env['res.partner'].search([('vat', '=', vat)], limit=1)
                        if not partner:
                            partner = self.env['res.partner'].create({'name': 'Unknown', 'vat': vat})
                    elif i > 0 and line[0].strip().lower() != 'formularios presentados':
                        # Validate line length to avoid index errors
                        if len(line) < 10:
                            _logger.error("Invalid data line at index %s: %s", i, line)
                            continue

                        # Create SII data record
                        self.create({
                            'partner_id': partner.id,
                            'tipo_contribuyente': line[1].strip(),
                            'tipo': line[3].strip(),
                            'giro_informado': line[5].strip(),
                            'codigo_actividad_informado': line[7].strip(),
                            'oficina_tramites': line[9].strip(),
                        })
            _logger.info("CSV import completed successfully.")
        except Exception as e:
            _logger.error("Error importing CSV file: %s", e)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    sii_data_ids = fields.One2many('sii.data', 'partner_id', string='Datos del SII')
