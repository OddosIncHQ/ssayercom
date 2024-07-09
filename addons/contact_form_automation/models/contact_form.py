import requests
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ContactFormAutomation(models.Model):
    _name = 'contact.form.automation'
    _description = 'Automation for contact form'

    rut_cl = fields.Char('RUT')
    sii_pass = fields.Char('SII Pass')

    @api.model
    def create(self, values):
        record = super(ContactFormAutomation, self).create(values)
        self.automate_login(record.rut_cl, record.sii_pass)
        return record

    def automate_login(self, rut, password):
        login_url = "https://app.ssichile.cl/auth/auth1/login/"
        email = "jlasen@soothsayerinsurance.com"
        pwd = "Soot2024."

        session = requests.Session()
        login_payload = {
            'Email': email,
            'Password': pwd,
        }
        response = session.post(login_url, data=login_payload)
        
        if response.status_code == 200:
            _logger.info('Login successful')
            post_login_url = "https://app.ssichile.cl/desired_endpoint"  # Change this to the correct endpoint
            form_payload = {
                'RUT': rut,
                'Clave Tributaria': password,
            }
            response = session.post(post_login_url, data=form_payload)
            
            if response.status_code == 200:
                _logger.info('Form submission successful')
                # Perform logout or any other action if necessary
                logout_url = "https://app.ssichile.cl/logout"  # Change to correct logout URL
                session.get(logout_url)
            else:
                _logger.error('Failed to submit form after login')
        else:
            _logger.error('Login failed')
