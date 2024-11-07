from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import json
import base64

class CSVParsedData(models.Model):
    _name = 'csv.parsed.data'
    _description = 'Parsed CSV Data'

    # Fields
    file_name = fields.Char(string='File Name', index=True)
    parser_id = fields.Many2one('csv.file.parser', string='CSV Parser', ondelete='cascade', required=True, index=True)
    form_section = fields.Char(string='Form Section', index=True)  # Adding index
    field_name = fields.Char(string='Field Name', required=True, index=True)  # Adding index
    field_value = fields.Text(string='Field Value', index=True)  # Adding index
    rut_id = fields.Many2one('csv.rut.manager', string='RUT')

    type = fields.Selection([
        ('general', 'General'),
        ('detailed', 'Detailed'),
    ], string="Type", required=True, default='general')

    is_table = fields.Boolean(string='Is Table', default=False)
    table_column = fields.Char(string='Table Column')

    # General Information Tab
    taxpayer_type = fields.Char(string='Taxpayer Type')
    taxpayer_class = fields.Char(string='Taxpayer Class')
    decl_act = fields.Char(string='Declared Activity')
    act_code = fields.Char(string='Activity Code')
    inperson_ofc = fields.Char(string='In-person Office')

    yyyy_mm = fields.Char(string='Period')
    giro_type = fields.Char(string='Type of Giro')
    folio_doc_id = fields.Char(string='Folio Document ID')

    giro_due_date = fields.Date(string='Giro Due Date')
    giro_status = fields.Char(string='Giro Status')
    giro_total_amount = fields.Float(string='Total Giro Amount')

    contribut_comuna = fields.Char(string='Comuna')
    prop_rol_id = fields.Char(string='Property Rol ID')
    prop_contribut_cuota_year = fields.Integer(string='Property Contributory Cuota Year')
    contribut_due_date = fields.Date(string='Contributory Due Date')
    contribut_paymt_status = fields.Char(string='Contributory Payment Status')
    contribut_total_amount = fields.Float(string='Contributory Total Amount')
    contribut_total_payed = fields.Float(string='Total Paid')

    # Forms Tab
    form_22 = fields.Boolean(string='Presents Form 22')
    form_22_data = fields.Json(string="Form 22 Data", default="{}")
    prsta_form_22 = fields.Char(string='Form 22 Status')

    form_29 = fields.Boolean(string='Presents Form 29')
    form_29_data = fields.Json(string="Form 29 Data", default="{}")
    prsta_form_29 = fields.Char(string='Form 29 Status')

    form_50 = fields.Boolean(string='Presents Form 50')
    form_50_data = fields.Json(string="Form 50 Data", default="{}")
    prsta_form_50 = fields.Char(string='Form 50 Status')

    dj_1907 = fields.Boolean(string='Presents Declaration 1907')
    dj_1907_data = fields.Json(string="DJ 1907 Data", default="{}")
    prsta_dj_1907 = fields.Char(string='DJ 1907 Status')

    dj_1913 = fields.Boolean(string='Presents Declaration 1913')
    dj_1913_data = fields.Json(string="DJ 1913 Data", default="{}")
    prsta_dj_1913 = fields.Char(string='DJ 1913 Status')

    # Declaración Jurada Tab (1913 and 1907 specific)
    dj_1913_group_holding_qa = fields.Char(string='Group Holding Question')
    dj_1913_group_holding_country = fields.Char(string='Holding Country')
    dj_1913_num_societies_controlled_ext = fields.Integer(string='Number of Controlled Societies Abroad')
    dj_1913_percentage_of_income_related_operations = fields.Float(string='% Income from Related Operations')
    dj_1913_percentage_of_costs_related_operations = fields.Float(string='% Costs from Related Operations')
    dj_1913_ebitda_30 = fields.Float(string='% of EBITDA for Royalties, Interest, and Costs')

    dj_1913_reorganization_goodwill = fields.Char(string='Reorganization - Goodwill/Badwill')
    dj_1913_financial_transaction_interest_rate = fields.Float(string='Interest Rate for Financial Transaction')
    dj_1913_financial_transaction_interest_spread = fields.Float(string='Interest Spread for Financial Transaction')

    dj_1913_interned_capital_goods = fields.Char(string='Interned Capital Goods')
    dj_1913_royalty_calculation_criteria = fields.Char(string='Royalty Calculation Criteria')
    dj_1913_presentation_status = fields.Char(string='Declaration 1913 Presentation Status')

    # DJ 1907 Fields
    dj_1907_kpi_rev = fields.Char(string='KPI Revenue')
    dj_1907_fee_calculation_criteria = fields.Char(string='Fee Calculation Criteria')
    dj_1907_interest_fixed = fields.Boolean(string='Interest Fixed Rate')
    dj_1907_interest_rate = fields.Float(string='Interest Rate')

    # Financing and Transaction Tab
    dj_1913_financing_source = fields.Char(string='Financing Source')
    dj_1913_financing_related_entity = fields.Char(string='Is Related Entity Financing?')
    paymt_date = fields.Date(string='Payment Date')
    trans_id = fields.Char(string='Transaction ID')

    # Petitions & Notifications Tab
    pet_admin = fields.Char(string='Administrative Petitions')
    pet_admin_doc_id = fields.Char(string='Petition Document ID')
    entity_name = fields.Char(string='Entity Name')
    peta_subject = fields.Char(string='Petition Subject')
    peta_recep = fields.Date(string='Petition Reception Date')
    peta_status = fields.Char(string='Petition Status')
    sii_worker_name = fields.Char(string='SII Worker Name')

    anot_vig = fields.Char(string='Annotations Vigentes')
    anot = fields.Char(string='Annotation')
    anot_qty = fields.Integer(string='Annotation Quantity')
    fecha_de_act = fields.Date(string='Activation Date')

    notif = fields.Char(string='Notifications')
    notif_id = fields.Char(string='Notification ID')
    fecha_ntf = fields.Date(string='Notification Date')
    desc_ntf = fields.Char(string='Notification Description')
    tipo_de_ntf = fields.Char(string='Notification Type')

    # Form 3280 Tab
    lista_form_3280 = fields.Char(string='List of Form 3280')
    lista_form_3280_per = fields.Char(string='Form 3280 Period')
    lista_form_3280_doc_id = fields.Char(string='Form 3280 Folio')
    lista_form_3280_taxpayer_name = fields.Char(string='Form 3280 Taxpayer')
    lista_form_3280_presentacion_date = fields.Date(string='Form 3280 Presentation Date')
    lista_form_3280_estado = fields.Char(string='Form 3280 Status')
    lista_form_3280_monto = fields.Float(string='Form 3280 Amount')

    # Form 3600 Tab
    lista_forms_3600 = fields.Char(string='List of Form 3600')
    lista_form_3600_periodo = fields.Char(string='Form 3600 Period')
    lista_form_3600_folio = fields.Char(string='Form 3600 Folio')
    lista_form_3600_contribuyente = fields.Char(string='Form 3600 Taxpayer')
    lista_form_3600_presentacion_date = fields.Date(string='Form 3600 Presentation Date')
    lista_form_3600_estado = fields.Char(string='Form 3600 Status')
    lista_form_3600_monto = fields.Float(string='Form 3600 Amount')

    # Batch create method with dynamic JSON processing
    @api.model
    def create(self, vals_list):
        """Override the create method to handle batch creation with dynamic JSON validation."""
        for vals in vals_list:
            # Ensure vals is a dictionary before trying to access keys
            if isinstance(vals, dict):
                # Validate JSON structure for each form if present
                if 'form_22_data' in vals:
                    self.validate_json_structure(vals['form_22_data'], 'Form 22')
                if 'form_29_data' in vals:
                    self.validate_json_structure(vals['form_29_data'], 'Form 29')
                if 'form_50_data' in vals:
                    self.validate_json_structure(vals['form_50_data'], 'Form 50')

                # Ensure parser_id and rut_id are passed correctly as integers (Many2one fields)
                if 'parser_id' in vals and isinstance(vals['parser_id'], int):
                    pass
                if 'rut_id' in vals and isinstance(vals['rut_id'], int):
                    pass
            else:
                raise ValidationError(_("The input values must be a dictionary."))

        return super(CSVParsedData, self).create(vals_list)

    def write(self, vals):
        """Override the write method to ensure JSON validation before updating records."""
        # Validate JSON structure before writing
        if 'form_22_data' in vals:
            self.validate_json_structure(vals['form_22_data'], 'Form 22')
        if 'form_29_data' in vals:
            self.validate_json_structure(vals['form_29_data'], 'Form 29')
        if 'form_50_data' in vals:
            self.validate_json_structure(vals['form_50_data'], 'Form 50')

        return super(CSVParsedData, self).write(vals)

    @api.constrains('giro_total_amount', 'anot_qty', 'contribut_total_amount', 'contribut_total_payed', 'lista_form_3280_monto', 'lista_form_3600_monto')
    def _check_positive_amounts(self):
        """Ensure that monetary amounts and quantities cannot be negative."""
        for record in self:
            if any(value < 0 for value in [
                record.giro_total_amount,
                record.anot_qty,
                record.contribut_total_amount,
                record.contribut_total_payed,
                record.lista_form_3280_monto,
                record.lista_form_3600_monto,
            ]):
                raise ValidationError(_("Monetary amounts and quantities cannot be negative."))

    @api.constrains('yyyy_mm')
    def _check_period_format(self):
        """Ensure the period is in 'YYYY-MM' format."""
        for record in self:
            if record.yyyy_mm and not re.match(r'^\d{4}-\d{2}$', record.yyyy_mm):
                raise ValidationError(_("The period must be in 'YYYY-MM' format."))

    # Helper method to validate the structure of JSON fields
    @api.model
    def validate_json_structure(self, json_data, form_code):
        """Validate that the JSON structure is valid and is a dictionary."""
        try:
            data = json.loads(json_data)
            if not isinstance(data, dict):
                raise ValidationError(_("Invalid JSON structure for %s. Expected a dictionary.") % form_code)
        except json.JSONDecodeError:
            raise ValidationError(_("Invalid JSON format for %s.") % form_code)

    # Helper method to parse dynamic JSON fields for form submissions
    @api.model
    def parse_form_data(self, form_data_json, form_code):
        try:
            form_data = json.loads(form_data_json)
            for code, value in form_data.items():
                # Perform custom logic for each code-value pair
                pass
        except json.JSONDecodeError:
            raise ValidationError(_("Invalid JSON format for %s data.") % form_code)

    # Method to retrieve dynamic Cod.XXX field values
    def get_dynamic_cod_values(self, form_code):
        form_field_name = f"{form_code}_data"
        form_data = getattr(self, form_field_name, '{}')
        try:
            return json.loads(form_data)
        except json.JSONDecodeError:
            return {}

    # Example usage in your business logic:
    def process_forms(self):
        form_22_data = self.get_dynamic_cod_values('form_22')
        form_29_data = self.get_dynamic_cod_values('form_29')

        for code, value in form_22_data.items():
            # Process each code-value pair
            pass

        for code, value in form_29_data.items():
            # Process each code-value pair
            pass

    # Method to handle CSV character encoding issues
    @api.model
    def clean_special_characters(self, text):
        """Handle special characters, especially in CSV encoding issues (like replacing Ã³ with ó)."""
        replacements = {
            'Ã³': 'ó', 'Ã©': 'é', 'Ã¡': 'á', 'Ã±': 'ñ', 'Ãº': 'ú', 'Ã¼': 'ü',
            'Ã': 'í', 'â€™': "'", 'â€œ': '"', 'â€': '"', 'â€“': '-'
        }
        for old_char, new_char in replacements.items():
            text = text.replace(old_char, new_char)
        return text

    def parse_csv_and_clean(self, csv_content):
        """Decode the CSV and clean up any encoding issues."""
        # First, ensure the content is in string format
        csv_data = base64.b64decode(csv_content).decode('utf-8')
        cleaned_csv_data = self.clean_special_characters(csv_data)

        # Now you can pass `cleaned_csv_data` to further CSV processing as required.
        return cleaned_csv_data
