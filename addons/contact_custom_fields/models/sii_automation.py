import requests
from odoo import models, api

class SSIAutomation(models.Model):
    _name = 'sii.automation'

    def login_and_fetch_data(self, rut, sii_pass):
        session = requests.Session()
        login_url = "https://app.ssichile.cl/"
        payload = {
            'email': 'jlasen@soothsayerinsurance.com',
            'password': 'Soot2024.'
        }
        session.post(login_url, data=payload)

        data_url = "https://app.ssichile.cl/data"
        data_payload = {
            'RUT': rut,
            'Clave Tributaria': sii_pass
        }
        response = session.post(data_url, data=data_payload)

        return response.json()  # Asumiendo que la respuesta es en formato JSON

    @api.model
    def process_contact_form(self, contact_id):
        contact = self.env['res.partner'].browse(contact_id)
        if contact.rut_cl and contact.sii_pass:
            data = self.login_and_fetch_data(contact.rut_cl, contact.sii_pass)
            # Procesar y guardar los datos obtenidos
            contact.write({
                'extra_data': data.get('extra_data_field')
            })
          
