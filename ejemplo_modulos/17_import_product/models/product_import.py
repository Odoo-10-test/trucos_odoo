# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
import os
import tempfile
import csv
from odoo.exceptions import UserError
import base64
import xlrd


class Product(models.Model):
    _name = 'product.import'
    _description = 'Product Import'

    name = fields.Char(string='Name', required=True)
    type = fields.Selection([('csv', 'Csv'), ('xls', 'Excel')], string='Type', required=True)
    file = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='File Name', required=True)
    imported = fields.Boolean(string='Imported', default=False, copy=False)

    def action_import(self):
        if self.type == 'csv':
            self.import_csv()
        else:
            self.import_xls()
        self.imported = True
        return True

    @api.model
    def validate_extesion_file(self, filename):
        name = os.path.splitext(filename)[1]
        return (True, name) if name in ['.csv'] else False

    @api.model
    def validate_extesion_file_excel(self, filename):
        name = os.path.splitext(filename)[1]
        return (True, name) if name in ['.xls','.xlsx'] else False

    def import_csv(self):
        if not self.validate_extesion_file(self.file_name):
            raise UserError(_("File should be CSV extension"))
        file_path = tempfile.gettempdir() + '/file.csv'
        data = self.file
        f = open(file_path, 'wb')
        f.write(base64.b64decode(data))
        f.close()
        archive = csv.DictReader(open(file_path))
        ProductObj = self.env['product.template']

        for line in archive:
            product_name = line.get('Product')
            product_code = line.get('Code')
            product_price = line.get('Price')
            cost = line.get('Cost')
            ProductObj.create({
                'name': product_name,
                'default_code': product_code,
                'list_price': product_price,
                'standard_price': cost,
                'type': 'product',
            })

    def import_xls(self):
        if not self.validate_extesion_file_excel(self.file_name):
            raise UserError(_("File should be Excel extension"))

        ProductObj = self.env['product.template']
        data = base64.b64decode(self.file)
        work_book = xlrd.open_workbook(file_contents=data)
        sheet = work_book.sheet_by_index(0)
        first_row = []

        for col in range(sheet.ncols):
            first_row.append(sheet.cell_value(0, col))

        cont = 0
        for count, row in enumerate(range(1, sheet.nrows), 2):
            try:
                val = {}
                cont += 1
                for col in range(sheet.ncols):
                    val[first_row[col]] = sheet.cell_value(row, col)
                code = str(val.get('Code').strip())
                price = float(val.get('Price', 0))
                cost = float(val.get('Cost', 0))
                product_name = val.get('Product', '')
                ProductObj.create({
                    'name': product_name,
                    'default_code': code,
                    'list_price': price,
                    'standard_price': cost,
                    'type': 'product',
                })
            except:
                raise UserError(_("There is an error in line" % (cont + 1)))




 
