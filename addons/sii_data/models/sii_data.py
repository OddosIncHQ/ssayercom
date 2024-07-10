from odoo import models, fields

class SiiData(models.Model):
    _name = 'sii.data'
    _description = 'SII Data'

    name = fields.Char(string='Name', required=True)
    vat_cl = fields.Char(string='RUT')
    sii_pass = fields.Char(string='SII Pass')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    company_id = fields.Many2one('res.company', string='Company')
    # Agrega otros campos según tus necesidades
    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    zip = fields.Char(string='ZIP')
    active = fields.Boolean(string='Active', default=True)
