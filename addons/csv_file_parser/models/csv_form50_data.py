from odoo import models, fields

class Form50DataModel(models.Model):
    _name = 'csv.form50.data'
    _description = 'Form 50 Data Model'

    parser_id = fields.Many2one('csv.file.parser', string='CSV Parser', ondelete='cascade')
    code = fields.Char(string='Code', required=True)
    value = fields.Char(string='Value', required=True)
