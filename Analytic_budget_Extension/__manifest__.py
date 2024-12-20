
{
    'name': 'Analytic Budget Extension',
    'version': '1.0.0',
    'author': 'Your Name',
    'category': 'Accounting/Accounting',
    'summary': 'Manage budgets with analytic accounts',
    'description': '''
This module extends Odoo's analytic accounting system by adding
budget planning, tracking, and variance analysis functionality.
    ''',
    'website': 'https://yourwebsite.com',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/budget_plan_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
