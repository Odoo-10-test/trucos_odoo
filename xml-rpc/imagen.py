# -- coding: utf-8 --
#************#
# Importación Clientes y Proveedores #
#************#

import os
import csv
import re
import xmlrpc.client
from urlparse import urlparse
import base64
import urllib2
import requests

url = 'http://167.71.12.101:8069'
db = 'db13-spain-sii'
username = 'admin'
password = 'passAzul'
path_file = 'imagenes.csv'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def get_image(url):
    if not url:
        return False
        # image = base64.b64encode(requests.get(url).content)
    # print url
    url_full = "Imagenes/" + url
    # print url_full

    with open(url_full, "rb") as f:
        data12 = f.read()
        UU = data12.encode("base64")
        UUU = base64.b64decode(UU)
    return UU


def _update_mass(estado):
    archive = csv.DictReader(open(path_file))
    cont = 0
    for field in archive:
        cont = cont + 1
        cod = field['codigo'].replace(" ", '')
        imagen = field['imagen']
        product = models.execute(db,uid,password,'product.template','search',[('default_code','=',cod)])
        product_id = product and product[0]
        if product_id and cod and imagen:
            print str(cont) + "--> " + str(product_id)+ "[" + cod + "]" + "  -  "  + str(imagen)
            full_path = imagen
            vals = {}
            vals['image_1920'] = get_image(full_path)
            # print vals
            do_write = models.execute(db,uid,password,'product.template', 'write', product_id, vals)

            # Categoría del Material
            """
            if field['  Categoría Material  ']:
                vals7 = field['  Categoría Material  '].strip()
                categoria = object_proxy.execute(DB,uid,PASS,'product.categoria.material','search',[('name','=',vals7)])
                categoria_id = categoria and categoria[0]
                vals['product_categoria_material_id'] = categoria_id"""
        else:
            print str(cont)

        #

def __main__():
    print 'Ha comenzado el proceso'
    _update_mass(True)
    print 'Ha finalizado la carga tabla'
__main__()

