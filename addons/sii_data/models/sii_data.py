from odoo import models, fields, api
import base64
import csv
from io import StringIO

class SiiData(models.Model):
    _name = 'sii.data'
    _description = 'SII Data'

    name = fields.Char(string='Name', required=True)
    activity_ids = fields.One2many('mail.activity', 'res_id', string='Activities', domain=[('res_model', '=', 'sii.data')])
    activity_state = fields.Selection([
        ('today', 'Today'),
        ('planned', 'Planned'),
        ('overdue', 'Overdue')
    ], string='Activity State')
    activity_type_id = fields.Many2one('mail.activity.type', string='Activity Type')
    activity_date_deadline = fields.Date(string='Deadline')
    activity_summary = fields.Char(string='Summary')
    activity_user_id = fields.Many2one('res.users', string='Responsible User')
    activity_calendar_event_id = fields.Many2one('calendar.event', string='Calendar Event')
    message_follower_ids = fields.Many2many(
        'res.partner', 
        'sii_data_res_partner_follower_rel', 
        'sii_data_id', 
        'partner_id', 
        string='Followers'
    )
    message_partner_ids = fields.Many2many(
        'res.partner', 
        'sii_data_res_partner_message_rel', 
        'sii_data_id', 
        'partner_id', 
        string='Partners'
    )
    message_ids = fields.One2many('mail.message', 'res_id', string='Messages', domain=[('model', '=', 'sii.data')])
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings', domain=[('res_model', '=', 'sii.data')])
    website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages', domain=[('model', '=', 'sii.data')])
    x_active = fields.Boolean(string='Active', default=True)
    x_studio_partner_id = fields.Many2one('res.partner', string='Partner')
    x_name = fields.Char(string='Custom Name')
    x_color = fields.Integer(string='Color')
    x_studio_company_id = fields.Many2one('res.company', string='Company')
    x_studio_notes = fields.Text(string='Notes')
    x_studio_date = fields.Date(string='Date')
    x_studio_value = fields.Float(string='Value')
    x_studio_stage_id = fields.Many2one('crm.stage', string='Stage')
    x_studio_kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')
    ], string='Kanban State')
    x_studio_currency_id = fields.Many2one('res.currency', string='Currency')
    x_studio_sequence = fields.Integer(string='Sequence')
    x_studio_priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High')
    ], string='Priority')
    x_studio_tag_ids = fields.Many2many('crm.tag', string='Tags')
    x_studio_partner_phone = fields.Char(string='Partner Phone')
    x_studio_partner_email = fields.Char(string='Partner Email')
    x_studio_mojo_file = fields.Binary(string='Mojo File')
    x_studio_mojo_file_filename = fields.Char(string='File Name')

    upload_file = fields.Binary(string='Upload File')
    upload_file_filename = fields.Char(string='Upload File Name')

    @api.onchange('x_studio_partner_id')
    def _onchange_partner_id(self):
        if self.x_studio_partner_id:
            self.x_studio_partner_phone = self.x_studio_partner_id.phone
            self.x_studio_partner_email = self.x_studio_partner_id.email

    @api.model
    def process_uploaded_file(self, file_content):
        # Implement the logic to process the uploaded file
        decoded_file = base64.b64decode(file_content)
        file_str = decoded_file.decode("utf-8")
        data = StringIO(file_str)
        csv_reader = csv.reader(data, delimiter=',')

        for row in csv_reader:
            # Example processing: assuming CSV with columns 'name' and 'value'
            name, value = row
            # Perform the desired actions with the row data
            # Example: create or update records based on the CSV data
            self.create({
                'name': name,
                # other fields to fill
            })

    def action_upload_file(self):
        self.ensure_one()
        if self.upload_file:
            self.process_uploaded_file(self.upload_file)
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
