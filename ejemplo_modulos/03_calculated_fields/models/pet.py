# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Pet(models.Model):
    _inherit = 'ej.pets'
    is_pretty_name = fields.Boolean(string='Pretty Name' ,
                                    compute='_compute_pretty_name')

    is_not_pretty_name = fields.Boolean(string='Pretty Name',
                                    compute='_compute_not_pretty_name',
                                    store=True)

    mydb = fields.Char(default=lambda self: self.env.cr.dbname, string='db')

    @api.depends('pretty_name')
    def _compute_pretty_name(self):
        for record in self:
            record.is_pretty_name = record.pretty_name

    @api.depends('pretty_name')
    def _compute_not_pretty_name(self):
        for record in self:
            record.is_not_pretty_name = not record.pretty_name