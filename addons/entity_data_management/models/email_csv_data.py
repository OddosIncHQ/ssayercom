from odoo import models, fields

class EmailCSVData(models.Model):
    _name = 'email.csv.data'
    _description = 'Email CSV Data'

    name = fields.Char(string='Name', required=True)
    csv_file = fields.Binary(string='CSV File', required=True)
    csv_file_name = fields.Char(string='CSV File Name')
    upload_datetime = fields.Datetime(string='Upload DateTime')
    upload_type = fields.Selection([
        ('type1', 'FetchMail'),
        ('type2', 'Manual')
    ], string='Upload Type')

    rut = fields.Char(string='RUT', help="RUT or RUN of the entity")
