from odoo import models, fields, api
import csv
import base64

class CsvImportWizard(models.TransientModel):
    _name = 'csv.import.wizard'
    _description = 'CSV Import Wizard'

    csv_file = fields.Binary(string='CSV File')

    @api.multi
    def import_csv(self):
        csv_data = base64.b64decode(self.csv_file)
        data = csv_data.decode('utf-8').splitlines()
        csv_reader = csv.reader(data)
        
        for row in csv_reader:
            # Parse and create records
            self.env['res.partner'].create({
                'name': row[0],
                'rut': row[1],
                'contribuyente_type': row[2],
                'empresa_type': row[3],
                'giro_informado': row[4],
                'codigo_actividad_informado': row[5],
                'oficina_tramites': row[6],
                # Add other fields as needed
            })

        return {'type': 'ir.actions.act_window_close'}
