# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import fields, models, api, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_make_move_income(self):
        raise UserError(_('You can only execute this action from the product template'))

    def action_make_move_expense(self):
        raise UserError(_('You can only execute this action from the product template'))

    def action_view_move_entries(self):
        raise UserError(_('You can only execute this action from the product template'))


class ProductTemplate(models.Model):
    _inherit = "product.template"

    account_entry_ids = fields.Many2many('account.move', string='Entries')

    def action_make_move_income(self):
        lines_ids = [(0, 0, self._prepare_invoice_line_vals(self.list_price, 0, self.with_company(
            self.env.company).property_account_income_id.id, _('income'))),
                     (0, 0, self._prepare_invoice_line_vals(0, self.list_price, self.with_company(
                         self.env.company).property_account_expense_id.id, _('expense')))]
        self._helper_create_move(lines_ids)

    def action_make_move_expense(self):
        lines_ids = [(0, 0, self._prepare_invoice_line_vals(0, self.with_company(self.env.company).standard_price,
                                                            self.with_company(
                                                                self.env.company).property_account_income_id.id,
                                                            _('income'))),
                     (0, 0, self._prepare_invoice_line_vals(self.with_company(self.env.company).standard_price, 0,
                                                            self.with_company(
                                                                self.env.company).property_account_expense_id.id,
                                                            _('expense')))]
        self._helper_create_move(lines_ids)

    def _helper_create_move(self, lines_ids):
        move_vals = self._prepare_invoice_vals()
        move_vals.update({'line_ids': lines_ids})
        move = self.env['account.move'].create(move_vals)
        move.post()
        self.account_entry_ids = [(4, move.id)]

    def _prepare_invoice_vals(self):
        journal_id = self.env['account.journal'].search(
            [('type', '=', 'general'), ('company_id', '=', self.env.company.id)], limit=1)
        if not journal_id:
            raise UserError(_('Please define an accounting general journal for this company.'))
        vals = {
            'move_type': 'entry',
            'company_id': self.env.company.id,
            'journal_id': journal_id.id,
            'currency_id': self.env.company.currency_id.id,
            'line_ids': [],
            'ref': self.name,
        }
        return vals

    def _prepare_invoice_line_vals(self, credit, debit, account_id, operation):
        if not account_id:
            raise UserError(_('Please define an %s account for this product.') % operation)
        vals = {
            'display_type': 'product',
            'name': self.name,
            'credit': credit,
            'debit': debit,
            'account_id': account_id,
        }
        return vals

    def action_view_move_entries(self):
        action = self.env.ref('account.action_move_journal_line').read()[0]
        action['domain'] = [('id', 'in', self.account_entry_ids.ids)]
        return action
