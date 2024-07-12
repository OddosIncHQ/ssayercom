import csv
from odoo import models, fields, api

class SiiData(models.Model):
    _name = 'sii.data'
    _description = 'Datos extraídos del SII'

    name = fields.Char(string='Name', required=True)
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
                if i == 0:  # Asumimos que la primera línea tiene el VA
