from odoo import http
from odoo.http import request

class ContactFormController(http.Controller):

    @http.route('/website/form', type='http', auth='public', website=True)
    def handle_contact_form(self, **post):
        # Obtener los datos del formulario
        rut_cl = post.get('rut_cl')
        sii_pass = post.get('sii_pass')

        # Crear el registro en el modelo
        request.env['contact.form.automation'].sudo().create({
            'rut_cl': rut_cl,
            'sii_pass': sii_pass,
        })

        return request.render('your_module_name.success_page')
