# -- coding: utf-8 --
#************#
# Modificar precios
#************#

import xmlrpc.client
import json
import csv
import time
from itertools import chain
import logging

# Servidor Demo
demo_host = 'demo.odoo.com'
demo_port = 80
demo_db = 'demo-5668855'
demo_user = 'admin'
demo_password = 'azul'
demo_url = 'http://%s:%d/xmlrpc/2/' % (demo_host, demo_port)
demo_common_proxy = xmlrpc.client.ServerProxy(demo_url + 'common')
demo_object_proxy = xmlrpc.client.ServerProxy(demo_url + 'object')
demo_uid = demo_common_proxy.login(demo_db, demo_user, demo_password)
if demo_uid:
    print('Conectado al servidor demo')

# Servidor Producción
pro_host = 'pro.odoo.com'
pro_port = 80
pro_db = 'production-713973'
pro_user = 'admin'
pro_password = 'verde'
pro_url = 'http://%s:%d/xmlrpc/2/' % (pro_host, pro_port)
pro_common_proxy = xmlrpc.client.ServerProxy(pro_url + 'common')
pro_object_proxy = xmlrpc.client.ServerProxy(pro_url + 'object')
pro_uid = pro_common_proxy.login(pro_db, pro_user, pro_password)
if pro_uid:
    print('Conectado al servidor pro')




def _create(estado):
    if estado is True:
        contador = 0
        model_find = 'product.product'
        products = demo_object_proxy.execute(demo_db,demo_uid,demo_password,model_find,'search',[('active','=',True)])
        if products:
            for item in products:
                contador += 1
                if item != 0 and contador > 1348:
                    demo_product_find = demo_object_proxy.execute(demo_db, demo_uid, demo_password, model_find, 'search_read', [('id','=',item) ])
                    
                    name = demo_product_find[0]['name']
                    display_name = demo_product_find[0]['display_name']
                    barcode = demo_product_find[0]['barcode']
                    default_code = demo_product_find[0]['default_code']
                    description = "31/08/2020"
                    active = demo_product_find[0]['active']
                    
                    vals = {}
                    vals['name'] = name
                    vals['display_name'] = display_name
                    vals['barcode'] = barcode
                    vals['default_code'] = default_code
                    vals['description'] = description
                    vals['active'] = active

                    print(vals)
                    # revisamos que no exista mas productos con ese barcode
                    if barcode != False:
                        products2 = pro_object_proxy.execute(pro_db,pro_uid,pro_password,model_find,'search',[('barcode','=',barcode)])
                        for item2 in products2:
                            vals2 = {}
                            vals2['barcode'] = False
                            print(vals2)
                            do_write2 = pro_object_proxy.execute(pro_db, pro_uid, pro_password,'product.product', 'write',item2, vals2 )
                            if do_write2:
                                print("Existe", item2)
                        

                    # Cambiando en Producción
                    do_write = pro_object_proxy.execute(pro_db, pro_uid, pro_password,'product.product', 'write',item, vals )
                    print(item, name, display_name, barcode, default_code, description)
                    
                    print("Contador ========>", contador)
                    
        print(contador);

def main():
    print("Ha comenzado el proceso")
    _create(True)
    print('Ha finalizado la carga tabla')
main()
