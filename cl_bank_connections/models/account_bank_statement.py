# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import requests
import json

from datetime import date, datetime, timedelta


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    def get_api_key(self):
        api_key = self.env['res.users'].search([
            ('fintoc_api_key', '!=', False)
        ], limit=1).fintoc_api_key

        return api_key

    def ListAccounts(self):

        journals = self.env['account.journal'].search([
            ('fintoc_link_token', '!=', False)
        ])

        accounts_list = []

        if journals:
            for journal in journals:
                fintoc_link_token = journal.fintoc_link_token
                url = f"https://api.fintoc.com/v1/accounts/?link_token={fintoc_link_token}"

                headers = {
                    "accept": "application/json",
                    "Authorization": self.get_api_key()
                }

                response = requests.get(url, headers=headers)
                data = response.json()

                journal_account = journal.bank_account_id.acc_number

                for list in data:
                    if journal_account == list['number']:
                        journal.bank_account_id.fintoc_token = list['id']

                        info = {
                            'acc_token': list['id'],
                            'fintoc_link_token': fintoc_link_token,
                            'journal': journal,
                        }

                        accounts_list.append(info)

        return accounts_list

    def ListMovements(self):

        accounts = self.ListAccounts()

        for account in accounts:

            fintoc_link_token = 'link_token=' + account['fintoc_link_token']

            url = f"https://api.fintoc.com/v1/accounts/{account['acc_token']}/movements?{fintoc_link_token}"

            headers = {
                "accept": "application/json",
                "Authorization": self.get_api_key()
            }

            response = requests.get(url, headers=headers)

            movements = response.json()

            if movements:

                bank_statements = self.env['account.bank.statement.line'].search([
                    ('journal_id','=', account['journal'].id)
                ])

                if bank_statements:

                    bank_reconciliation_lines_list = []

                    today_date = fields.Date.today().strftime('%Y-%m-%d')

                    for move in movements:

                        if move['id'] not in [line.fintoc_id for line in bank_statements]:
                            date_str = move['post_date']
                            parsed_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                            formatted_date = parsed_date.strftime('%Y-%m-%d')

                            today_date = fields.Date.today().strftime('%Y-%m-%d')

                            bank_reconciliation_lines = {
                                'fintoc_id': move['id'],
                                'journal_id': account['journal'].id,
                                'date': formatted_date,
                                'payment_ref': move['description'],
                                'amount': move['amount'],
                            }

                            bank_reconciliation_lines_list.append((0, 0, bank_reconciliation_lines))

                    bank_reconciliation = {
                        'journal_id': account['journal'].id,
                        'date': today_date,
                        'line_ids': bank_reconciliation_lines_list,
                    }

                    self.env['account.bank.statement'].create(bank_reconciliation)

                else:

                    bank_reconciliation_lines_list = []

                    today_date = fields.Date.today().strftime('%Y-%m-%d')

                    for move in movements:
                        date_str = move['post_date']
                        parsed_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                        formatted_date = parsed_date.strftime('%Y-%m-%d')

                        bank_reconciliation_lines = {
                            'fintoc_id': move['id'],
                            'journal_id': account['journal'].id,
                            'date': formatted_date,
                            'payment_ref': move['description'],
                            'amount': move['amount'],
                        }

                        bank_reconciliation_lines_list.append((0, 0, bank_reconciliation_lines))

                    bank_reconciliation = {
                        'journal_id': account['journal'].id,
                        'date': today_date,
                        'line_ids': bank_reconciliation_lines_list,
                    }

                    self.env['account.bank.statement'].create(bank_reconciliation)

            else:
                continue


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    fintoc_id = fields.Char('Fintoc ID')