from odoo import models, fields

class CSVAdditionalData(models.Model):
    _name = 'csv.additional.data'
    _description = 'Additional Parsed CSV Data'

    # This field links additional data to the CSV parser
    parser_id = fields.Many2one('csv.file.parser', string='CSV Parser', ondelete='cascade')

    # Fields to store additional parsed data from the CSV file
    column_name = fields.Char(string='Column Name')
    column_value = fields.Char(string='Column Value')
