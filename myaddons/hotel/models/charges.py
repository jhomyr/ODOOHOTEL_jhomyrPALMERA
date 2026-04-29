#myaddons/hotel/models/charges.py - stores guest charges

# - *- coding: utf-8 -*-
from odoo import models, fields
#myaddons/hotel/models/charges.py 

class Charge(models.Model):
    _name = 'hotel.charge'
    _description = 'hotel charges/accounts master lists'
    _order = "name"

    name = fields.Char("Account Name")
    description = fields.Char("Account Description")
    paymentaccount = fields.Boolean("Payment Account", default=False)

    company_id = fields.Many2one(
        'res.company', 
        string="Company", 
        required=True, 
        index=True,
        default=lambda self: self.env.company.id) #auto-assign current us 