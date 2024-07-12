from odoo import models, fields

class MainModel(models.Model):
    _inherit = 'res.partner'

    # Additional fields specific to the SoothSayer module
    contribuyente_type = fields.Char(string='Tipo de contribuyente')
    empresa_type = fields.Char(string='Tipo')
    giro_informado = fields.Text(string='Giro informado')
    codigo_actividad_informado = fields.Char(string='Código de actividad informado')
    oficina_tramites = fields.Text(string='Oficina para trámites presenciales')
    form_ids = fields.One2many('soothsayer.form', 'main_id', string='Formularios Presentados')
