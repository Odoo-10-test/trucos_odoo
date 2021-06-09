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

host = '127.0.0.1'
port = 8069
db = 'db14-spain'
user = 'admin'
password = 'admin'
url = 'http://%s:%d/xmlrpc/2/' % (host, port)

common_proxy = xmlrpc.client.ServerProxy(url + 'common')
object_proxy = xmlrpc.client.ServerProxy(url + 'object')
uid = common_proxy.login(db, user, password)
if uid:
    print('Conectado al servidor maestro')

path_file = 'codigos.csv'

def _create(estado):
    if estado is True:
        archive = csv.DictReader(open(path_file))
        cont = 0
        for field in archive:
            print(field)
            cont += 1
            default_code = field['\ufeffCOD'].strip()
            product_find = object_proxy.execute(db,uid,password,'product.template','search',[('default_code','=',default_code)])
            if product_find:
                PRE = field['PRE CODIGO'].strip()
                CODIGO_PROVEEDOR = field['CODIGO PROVEEDOR'].strip()
                barcode =  PRE + CODIGO_PROVEEDOR
                product_f2 = object_proxy.execute(db,uid,password,'product.template','search',[('barcode','=',barcode)])
                if product_f2:
                    print("Ya existe")
                else:
                    do_write = object_proxy.execute(db,uid,password,'product.template', 'write', product_find, {'barcode': barcode})
                print(cont," ====> ",default_code)
            else:
                print(cont," ==  NO  ==> ",default_code)


def main():
    print("Ha comenzado el proceso")
    _create(True)
    print('Ha finalizado la carga tabla')
main()
