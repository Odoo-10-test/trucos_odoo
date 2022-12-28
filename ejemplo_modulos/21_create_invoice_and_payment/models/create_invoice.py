#-*- coding: utf-8 -*-

import os
import csv
import tempfile
from odoo.exceptions import UserError
from odoo import fields, models, api, _
import base64
from datetime import datetime, date
import xlrd


class CreateInvoice(models.Model):
    _name = "create.invoice.model"
    _description = "Create Invoice"
    _order = 'id desc'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    name = fields.Char(string='Name', default=_("New"))
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
    state = fields.Selection([('draft', 'Draft'), ('invoice', 'Invoice'),('payment','Payment'),('reconcile','Reconcile')], string='State', default='draft')
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True)
    payment_journal_id = fields.Many2one('account.journal', string='Payment Journal', domain="[('type', 'in', ('bank', 'cash')), ('company_id', '=', company_id)]")


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
                'create.invoice.model') or _('New')
        faq = super().create(vals)
        return faq

    def action_create_invoice(self):
        self.ensure_one()
        invoice_vals = self._prepare_invoice_vals()
        invoice_vals.update({'invoice_line_ids': [(0, 0, self._prepare_invoice_line_vals())]})
        self.invoice_id = self.env['account.move'].create(invoice_vals).id
        self.invoice_id.action_post()
        self.state = 'invoice'

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

    def action_create_payment(self):
        payment_obj = self.env['account.payment']
        payment_type = 'inbound'
        payment_method = self.payment_journal_id.available_payment_method_ids.filtered_domain([('payment_type', '=', 'inbound')])[0]
        partner_type = 'customer'
        vals = {
            'partner_id': self.partner_id.id,
            'payment_type': payment_type,
            'amount': self.invoice_id.amount_total,
            'date': self.date_invoice,
            'partner_type': partner_type,
            'ref': self.invoice_id.name,
            'journal_id': self.payment_journal_id.id,
            'payment_method_id': payment_method.id
        }
        payment = payment_obj.create(vals)
        payment.action_post()
        self.payment_id = payment.id
        self.state = 'payment'

    def action_reconcile(self):
        for line in self.payment_id.line_ids:
            if line.credit > 0:
                line_id = line.id
        try:
            self.invoice_id.js_assign_outstanding_line(line_id)
        except:
            pass
        self.state = 'reconcile'




