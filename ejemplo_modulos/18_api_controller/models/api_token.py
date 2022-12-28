# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ApiToken(models.Model):
    _name = 'api.token'
    _description = 'Api Token'

    name = fields.Char(string='Name', required=True)
    token = fields.Char(string='Token', required=True)
    is_active = fields.Boolean(string='Is active', default=True)
 
