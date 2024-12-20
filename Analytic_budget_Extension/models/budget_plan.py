
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BudgetPlanLine(models.Model):
    _name = 'budget.plan.line'
    _description = 'Budget Plan Line'

    budget_plan_id = fields.Many2one('budget.plan', string='Budget Plan', required=True)
    description = fields.Char(string='Description')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    unit_measure = fields.Selection([
        ('pcs', 'Pieces'),
        ('kg', 'Kilograms'),
        ('l', 'Liters'),
        ('m', 'Meters'),
    ], string='Unit of Measure', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    unit_price = fields.Float(string='Unit Price', required=True)
    total_item_currency = fields.Float(string='Total (Item Currency)', compute='_compute_totals', store=True)
    total_budget_currency = fields.Float(string='Total (Budget Currency)', compute='_compute_totals', store=True)
    total_company_currency = fields.Float(string='Total (Company Currency)', compute='_compute_totals', store=True)

    @api.depends('quantity', 'unit_price', 'currency_id', 'budget_plan_id.analytic_account_id.company_id.currency_id')
    def _compute_totals(self):
        for line in self:
            line.total_item_currency = line.quantity * line.unit_price
            if line.currency_id:
                company_currency = line.budget_plan_id.analytic_account_id.company_id.currency_id
                line.total_budget_currency = line.currency_id._convert(
                    line.total_item_currency,
                    line.currency_id,
                    line.budget_plan_id.analytic_account_id.company_id,
                    fields.Date.today()
                )
                line.total_company_currency = line.currency_id._convert(
                    line.total_item_currency,
                    company_currency,
                    line.budget_plan_id.analytic_account_id.company_id,
                    fields.Date.today()
                )
            else:
                line.total_budget_currency = line.total_item_currency
                line.total_company_currency = line.total_item_currency
