# -- coding: utf-8 --
#************#
# Importación Clientes y Proveedores #
#************#

import os
import csv
import xmlrpclib
import re
from urlparse import urlparse
import base64
import urllib2
import requests


HOST='127.0.0.1'
PORT=8069
DB='mh'
USER='admin'
PASS='admin'
path_file = 'productos.csv'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

# archive = csv.DictReader(open(path_file))

def get_image(url):
    if not url:
        return False
    try:
        image = base64.b64encode(requests.get(url).content)
    except Exception as exc:
        image = False
    return image

def _create(estado):
    if estado is True:
        archive = csv.DictReader(open(path_file))
        cont = 1

        for field in archive:
            vals = {}


            product_find = object_proxy.execute(DB,uid,PASS,'product.template','search',[('barcode','=',field['barcode'])])
            if product_find:
                my_product = object_proxy.execute(DB,uid,PASS,'product.template','read', product_find,[])
                producto_a_buscar =  my_product[0]['name']
                # print "->" + producto_a_buscar

                product_id =  product_find[0]
                do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write', product_id, {'list_price': field['lst_price'].replace(",", ''),'name': field['name'],'meli_description': field['meli_description']})

                # Editamos la traduccion
                nombre = producto_a_buscar
                # print nombre
                product_find_traducido = object_proxy.execute(DB,uid,PASS,'ir.translation','search',[('value','=',nombre)])
                # print product_find_traducido
                for termino in product_find_traducido:
                    print termino
                    do_write = object_proxy.execute(DB,uid,PASS,'ir.translation', 'unlink', termino)

                    # Vinilo MATTHEWS, DAVE & TIM REYNOLDS - LIVE AT LUTHER COLLEG


                if do_write:
                    print str(cont) + "--" + str(field['barcode']) + "--> Editado"
            else:
                # Registramos los campos
                vals['barcode'] = field['barcode']
                vals['name'] = field['name']
                vals['default_code'] = field['default_code']
                vals['meli_description'] = field['meli_description']
                vals['list_price'] = field['lst_price']
                full_path = field['image_medium']

                vals['image_medium'] = get_image(full_path)
                vals['meli_imagen_logo'] = field['meli_imagen_logo']

                vals['meli_available_quantity'] = field['meli_available_quantity']
                vals['meli_post_required'] = True
                vals['meli_pub'] = True
                if field['meli_category']:
                    meli_category_find = object_proxy.execute(DB,uid,PASS,'mercadolibre.category','search',[('name','=',field['meli_category'])])
                    if meli_category_find:
                        meli_category_id =  meli_category_find[0]
                        vals['meli_category'] = meli_category_id

                product_id = object_proxy.execute(DB,uid,PASS,'product.template','create',vals)
                if product_id:
                    print str(cont) + "--" + str(field['barcode']) + "--> Insertado"
            cont += 1


def main():
    print 'Ha comenzado el proceso'
    _create(True)
    print 'Ha finalizado la carga tabla'
main()





