# -*- coding: utf-8 -*-
{
    'name': "Hotel",
    'summary': "Hotel Management System",
    'description': "Hotel Guest Registration and Billing System",
    'author': "Jhomyr",
    'website': "https://www.odoo.com",
    
    'category': 'Uncategorized',
    'version': '19.0.1.0.0',

    'depends': ['base', 'web'],


    'license': 'LGPL-3',


    'data': [
        'security/ir.model.access.csv',
        'views/mainmenu.xml',
        'views/guestregistration.xml',
        'views/guests.xml',
        'views/rooms.xml',
        'views/roomtypes.xml',
        'views/charges.xml',
        
    ],

    'installable': True,
    'application': True, 
}