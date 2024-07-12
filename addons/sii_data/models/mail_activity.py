from odoo import models, fields, api

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    activity_date_deadline = fields.Date(string='Deadline')
    activity_type_id = fields.Many2one('mail.activity.type', string='Activity Type')
    activity_user_id = fields.Many2one('res.users', string='Assigned to')
    activity_summary = fields.Text(string='Summary')
