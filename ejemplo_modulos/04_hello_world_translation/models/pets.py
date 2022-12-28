# -*- coding: utf-8 -*-
from odoo import api, fields, models

class pets(models.Model): 
    _name = 'ej.pets' 
    name = fields.Char(string='name', required=True)
    age = fields.Integer(string='age')
    color = fields.Char(string='color')
    type = fields.Selection([('small', 'Small'),
                             ('medium', 'Medium'),
                             ('big', 'Big')], string='type', default="small", required=True)

 
