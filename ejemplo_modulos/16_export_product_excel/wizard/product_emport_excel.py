#-*- coding: utf-8 -*-

from odoo import fields, models, api, _
import base64
from io import BytesIO
from odoo.tools.misc import xlwt


class ProductExportExcel(models.TransientModel):
    _name = "product.export.excel"
    _description = "Export Product Excel"

    product_type = fields.Selection([('product', 'Stockable Product'), ('consu', 'Consumable'), ('service', 'Service'),('all','All')], string='Product Type', default='all')

    def export_product_excel(self):
        domain = []
        if self.product_type != 'all':
            domain.append(('type', '=', self.product_type))
        products = self.env['product.product'].search(domain)
        return self._helper_export_product_excel(products)

    def _helper_export_product_excel(self,products):
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet(_("Product"))
        file_name = _("Products")
        style_border_table_top = xlwt.easyxf(
            'borders: left thin, right thin, top thin, bottom thin; font: bold on;')
        style_border_table_details = xlwt.easyxf('borders: bottom thin;')
        style_border_table_details_red = xlwt.easyxf('borders: bottom thin; font: colour red, bold True;')

        worksheet.write(0, 0, _("Code"), style_border_table_top)
        worksheet.write_merge(0, 0, 1, 3, _("Product"), style_border_table_top)
        worksheet.write(0, 4, _("Price"), style_border_table_top)
        worksheet.write(0, 5, _("Cost"), style_border_table_top)

        row = 1
        for product in products:
            style = style_border_table_details
            if not product.default_code:
                style = style_border_table_details_red
            worksheet.write(row, 0, product.default_code or '', style)
            worksheet.write_merge(row, row, 1, 3, str(product.name), style)
            worksheet.write(row, 4, product.list_price, style)
            worksheet.write(row, 5, product.with_company(self.env.company).standard_price, style)
            row += 1

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        data_b64 = base64.encodebytes(data)
        doc = self.env['ir.attachment'].create({
            'name': '%s.xls' % (file_name),
            'datas': data_b64,
        })
        return {
            'type': "ir.actions.act_url",
            'url': "web/content/?model=ir.attachment&id=" + str(
                doc.id) + "&filename_field=name&field=datas&download=true&filename=" + str(doc.name),
            'no_destroy': False,
        }
