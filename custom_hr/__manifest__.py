# -*- coding: utf-8 -*-
{
    'name': "Employee Address",
    'summary': """Employee Private Address""",

    'author': "Smarten Technologies",
    'website': "https://www.smarten.com.np",
    'category': 'Employees',
    'sequence': '-105',
    'version': '18.1',
    'license': 'LGPL-3',

    'depends': [
        'base','hr','contacts',
    ],

    'data': [
        "security/ir.model.access.csv",
        "views/employee_address.xml",
        "views/province.xml",
        "views/district_view.xml",
        "views/municipality_view.xml",
        "views/ward.xml",
    ],
    'application': True,
    'installable': True,
}