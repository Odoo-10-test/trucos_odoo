# -*- coding: utf-8 -*-
from odoo import api, fields, models

class EjPet(models.Model):
    _inherit = 'ej.pet'
    pretty_name = fields.Boolean(string='Pretty Name')
    my_age = fields.Integer(string='My Age')
