# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Assets Management',
    'description': """
Assets management
=================
Manage assets owned by a company or a person.
Keeps track of depreciations, and creates corresponding journal entries.

    """,
    'category': 'Accounting/Accounting',
    'sequence': 32,
    'depends': ['account_reports'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_tax_asset_views.xml',
    ],
    'license': 'OEEL-1',
    'auto_install': True,
    'application': True,
}
