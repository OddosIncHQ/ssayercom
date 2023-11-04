# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    fintoc_api_key = fields.Char(string="Fintoc Api Key")
