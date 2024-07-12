import csv
from odoo import models, fields, api

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
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

            partner = None
            for i, line in enumerate(data):
                if i == 0:  # Asumimos que la primera línea tiene el VAT
                    vat = line[1]
                    partner = self.env['res.partner'].search([('vat', '=', vat)], limit=1)
                    if not partner:
                        partner = self.env['res.partner'].create({'name': 'Unknown', 'vat': vat})
                elif i > 0 and line[0].lower() != 'formularios presentados':
                    # Crear el registro de datos del SII
                    self.create({
                        'partner_id': partner.id,
                        'tipo_contribuyente': line[1],
                        'tipo': line[3],
                        'giro_informado': line[5],
                        'codigo_actividad_informado': line[7],
                        'oficina_tramites': line[9],
                    })

class ResPartner(models.Model):
    _inherit = 'res.partner'

    sii_data_ids = fields.One2many('sii.data', 'partner_id', string='Datos del SII')
