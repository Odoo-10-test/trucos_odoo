# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from datetime import date, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        params = self.env['ir.config_parameter'].sudo()
        propose_validity_date = params.get_param('propose_order_validity')
        days_ahead = params.get_param('days_ahead')
        if propose_validity_date == 'True':
            res['validity_date'] = date.today() + timedelta(days=int(days_ahead))
        return res



 
