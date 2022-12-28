#-*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ModifyProduct(models.TransientModel):
    _name = "modify.product.wzd"
    _description = "Modify Product"

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, readonly=True)
    sale_tax_id = fields.Many2one('account.tax', string='Sale Tax', domain="[('type_tax_use', '=', 'sale'),('company_id', '=', company_id)]")
    purchase_tax_id = fields.Many2one('account.tax', string='Purchase Tax', domain="[('type_tax_use', '=', 'purchase'),('company_id', '=', company_id)]")

    def action_modify_products(self):
        if not self.sale_tax_id and not self.purchase_tax_id:
            raise UserError(_('You must select at least one tax to modify.'))
        tmpl_ids = self.env.context.get('active_ids', [])
        for template in self.env['product.template'].browse(tmpl_ids):
            if self.sale_tax_id:
                template.taxes_id = self.sale_tax_id
            if self.purchase_tax_id:
                template.supplier_taxes_id = self.purchase_tax_id
