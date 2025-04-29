# -*- coding: utf-8 -*-
{
    'name': "custom_employee",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Smarten Technologies",
    'website': "https://www.smarten.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_actions_server_data.xml',
        'views/views.xml',
        'views/employee_address.xml',
        'views/employee_batch_transfer_wizard.xml',
        'views/send_mail.xml'
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

