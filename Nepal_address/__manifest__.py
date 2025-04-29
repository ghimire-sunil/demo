# -*- coding: utf-8 -*-
{
    'name': "employee_address_nepal",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Smarten Technologies",
    'website': "https://www.smarten.com",


    # for the full list
    'category': 'Employee',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/employee_address.xml',
        'views/district.xml',
        'views/municipality.xml',
        'views/province.xml',
        'views/ward.xml'
        
    ],
}

