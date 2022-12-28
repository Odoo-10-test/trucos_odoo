#-*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import timedelta
from odoo.exceptions import UserError


class SearchSale(models.TransientModel):
    _name = "search.sale.by.date"
    _description = "Search Sale By Date"

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    date = fields.Date(string='Sale Date', required=True, default=fields.Date.context_today)
    days_ago = fields.Integer(string='Days ago', default=0)

    def action_view_sales(self,orders):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['domain'] = [('id', 'in', orders.ids)]
        action['context'] = {'create': False}
        return action

    def action_search_sales(self):
        date = self.date
        if self.days_ago > 0:
            date = self.date - timedelta(days=self.days_ago)
        orders = self.env['sale.order'].search([('date_order', '<=', date), ('company_id', '=', self.company_id.id)])
        if orders:
            return self.action_view_sales(orders)

        raise UserError(_('No sales found for this date'))



