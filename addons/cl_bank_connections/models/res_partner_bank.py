# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    fintoc_token = fields.Char('Fintoc Token')