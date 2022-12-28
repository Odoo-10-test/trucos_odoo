#-*- coding: utf-8 -*-

import os
import csv
import tempfile
from odoo.exceptions import UserError
from odoo import fields, models, api, _
import base64
from datetime import datetime, date
import xlrd


class CreateInvoice(models.TransientModel):
    _name = "create.invoice"

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain="[('type', '=', 'sale'), ('company_id', '=', company_id)]")
    date_invoice = fields.Date(string='Invoice Date', required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    invoice_payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    notes = fields.Text(string='Notes')
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price', default=0.0)

    def action_create_invoice(self):
        self.ensure_one()
        invoice_vals = self._prepare_invoice_vals()
        invoice_vals.update({'invoice_line_ids': [(0, 0, self._prepare_invoice_line_vals())]})
        invoice = self.env['account.move'].create(invoice_vals)
        return self.action_view_invoice(invoice)

    def _prepare_invoice_vals(self):
        vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'fiscal_position_id': self.partner_id.property_account_position_id and self.partner_id.property_account_position_id.id or False,
            'company_id': self.company_id.id,
            'invoice_date': self.date_invoice,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'invoice_payment_term_id': self.invoice_payment_term_id.id if self.invoice_payment_term_id else False,
            'invoice_line_ids': [],
            'narration': self.notes
        }
        return vals

    def _prepare_invoice_line_vals(self):
        vals = {
            'product_id': self.product_id.id,
            'quantity': self.quantity,
            'display_type': 'product',
            'price_unit': self.price_unit,
            'analytic_distribution': {str(self.analytic_account_id.id): 100} if self.analytic_account_id else False,
            'name': self.product_id.name,
        }
        return vals

    def action_view_invoice(self, invoice):
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = invoice.id
        return action




