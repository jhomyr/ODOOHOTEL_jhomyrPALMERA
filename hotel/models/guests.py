# -*- coding: utf-8 -*-

#guests.py
from datetime import date

from odoo import models, fields, api

class guests(models.Model):
    _name = 'hotel.guests'
    _description = 'hotel guests master list'
    _order ='lastname,firstname,middlename'

    lastname = fields.Char("Last Name")
    firstname = fields.Char("First Name")    
    middlename = fields.Char("Middle Name")        
    
    address_streetno  = fields.Char("Address /Street & No.")

    address_area =  fields.Char("Address /Bldg/Area/Brgy")
    
    address_city  = fields.Char("Address /City/Town")                        
    address_province  = fields.Char("Address /Province/State")
    zipcode  = fields.Char("Zip Code")
    contactno = fields.Char("Contact No.")
    email = fields.Char("Email")
    gender = fields.Selection([('FEMALE','Female'),('MALE','Male')],string="Gender")
    birthdate = fields.Date("Birthdate")
    photo = fields.Image("Guest Photo") 
    
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        index=True,
        default=lambda self: self.env.company,  # auto-assign current user's company
    )
    
    name = fields.Char(string='Guest Name', compute='_compute_name', store=True, index=True)
    @api.depends('lastname','firstname','middlename')
    def _compute_name(self):
        for rec in self:
            last = rec.lastname or ''
            first = rec.firstname or ''
            middle = rec.middlename or ''
            rec.name = f"{last}, {first} {middle}".strip().strip(',')


              
    age = fields.Integer(string='Age', compute='_compute_age')
    @api.depends('birthdate')
    def _compute_age(self):
        today = date.today()

        for rec in self:
            if rec.birthdate:
                birthdate = fields.Date.from_string(rec.birthdate)

                rec.age = (
                    today.year
                    - birthdate.year
                    - (
                        (today.month, today.day)
                        < (birthdate.month, birthdate.day)
                    )
                )
            else:
                rec.age = 0
              
              