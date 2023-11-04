# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    fintoc_link_token = fields.Char('Fintoc Link Token')
