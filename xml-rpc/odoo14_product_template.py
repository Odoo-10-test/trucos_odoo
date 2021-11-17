# -- coding: utf-8 --
#************#
# Importación Clientes y Proveedores #
#************#

import xmlrpc.client
import json
import csv
import time
from itertools import chain
import logging

host = 'santiago.123odoo.com'
port = 8069
db = 'db14-nog'
user = 'admin'
password = 'x1234567890'
url = 'http://%s:%d/xmlrpc/2/' % (host, port)

common_proxy = xmlrpc.client.ServerProxy(url + 'common')
object_proxy = xmlrpc.client.ServerProxy(url + 'object')

uid = common_proxy.login(db, user, password)

path_file = 'product.csv'

if uid:
    print('Conectado al servidor maestro')


def _create(estado):
    if estado is True:
        archive = csv.DictReader(open(path_file))
        cont = 0
        for field in archive:
            print(field)
            cont += 1
            """1"""
            default_code = field['default_code'].strip()
            name = field['name'].strip()
            barcode = field['barcode'].strip()

            """2"""
            product_find = object_proxy.execute(db,uid,password,'product.template','search',[('default_code','=',default_code)])
            if product_find:
                print("El producto existe")
            else:
                vals = {}
                vals['barcode'] = barcode
                vals['name'] = name
                vals['default_code'] = default_code

                product_id = object_proxy.execute(db,uid,password,'product.template','create',vals)
                if product_id:
                    print(cont,"INSERTADO PRODUCTO:", name)
                else:
                    print("Error")


def main():
    print("Ha comenzado el proceso")
    _create(True)
    print('Ha finalizado la carga tabla')
main()
