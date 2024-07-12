from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    rut_cl = fields.Char(string='RUT', required=True)
    sii_pass = fields.Char(string='SII Pass', required=True)
