from odoo import models, fields

class CSVDataNormalized(models.Model):
    _name = 'csv.data.normalized'
    _description = 'CSV Data Normalized'

    email_csv_data_id = fields.Many2one('email.csv.data', string='Email CSV Data', index=True)
    field_name = fields.Char(string='Field Name', index=True)
    field_value = fields.Char(string='Field Value', index=True)
    period = fields.Char(string='Period', index=True)
    year = fields.Char(string='Year', index=True)
    email_sender = fields.Char(string='Email Sender')

