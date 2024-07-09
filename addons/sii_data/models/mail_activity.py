from odoo import models, fields

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    activity_date_deadline = fields.Date(string='Activity Deadline')
