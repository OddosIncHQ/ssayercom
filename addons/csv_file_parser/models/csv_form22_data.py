from odoo import models, fields

class Form22DataModel(models.Model):
    _name = 'csv.form22.data'
    _description = 'Form 22 Data Model'

    parser_id = fields.Many2one('csv.file.parser', string='CSV Parser', ondelete='cascade')
    code = fields.Char(string='Code', required=True)
    value = fields.Char(string='Value', required=True)
