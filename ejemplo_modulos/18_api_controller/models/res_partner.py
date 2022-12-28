# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def prepare_api_partner_values(self, nif):
        partner = self.search([('vat','=',nif)],limit=1, order='id asc')
        if partner:
            return {
                'id': partner.id,  'name': partner.name,  'vat': partner.vat, 'zip': partner.zip,  'city': partner.city,
                'street': partner.street, 'street2': partner.street2, 'function': partner.function, 'email': partner.email,
                'website': partner.website,
            }
        return {}

 
