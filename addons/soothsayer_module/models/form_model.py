from odoo import models, fields

class FormModel(models.Model):
    _name = 'soothsayer.form'
    _description = 'Form Model'

    name = fields.Char(string='Formulario')
    year = fields.Char(string='Year')
    status = fields.Boolean(string='Presenta Formulario')
    main_id = fields.Many2one('res.partner', string='Main Record')
