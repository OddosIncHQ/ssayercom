from odoo import models, fields, api

class SiiData(models.Model):
    _name = 'sii.data'
    _description = 'SII Data'

    name = fields.Char(string='Name', required=True)
    vat_cl = fields.Char(string='RUT')
    sii_pass = fields.Char(string='SII Pass')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    company_id = fields.Many2one('res.company', string='Company')
    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    zip = fields.Char(string='ZIP')
    active = fields.Boolean(string='Active', default=True)

    # Campos adicionales necesarios
    activity_type_id = fields.Many2one('mail.activity.type', string='Activity Type')
    activity_date_deadline = fields.Date(string='Deadline')
    activity_user_id = fields.Many2one('res.users', string='Assigned to')
    activity_summary = fields.Text(string='Summary')
    activity_ids = fields.One2many('mail.activity', 'res_id', string='Activities', domain=[('res_model', '=', 'sii.data')])

    # Campos relacionados con los mensajes y seguidores
    message_follower_ids = fields.Many2many('res.partner', 'sii_data_follower_rel', 'sii_data_id', 'partner_id', string='Followers')
    message_partner_ids = fields.Many2many('res.partner', 'sii_data_partner_rel', 'sii_data_id', 'partner_id', string='Partners')
    message_ids = fields.One2many('mail.message', 'res_id', string='Messages', domain=[('model', '=', 'sii.data')])
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings', domain=[('res_model', '=', 'sii.data')])
    website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages', domain=[('model', '=', 'sii.data')])

    # Campos personalizados adicionales
    x_studio_partner_id = fields.Many2one('res.partner', string='Partner')
    x_studio_partner_phone = fields.Char(string='Partner Phone')
    x_studio_partner_email = fields.Char(string='Partner Email')

    upload_file = fields.Binary(string='Upload File')
    upload_file_filename = fields.Char(string='File Name')

    @api.model
    def action_upload_file(self):
        # Lógica para la acción del botón "Upload File"
        pass
