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


HOST='g1.123odoo.com'
PORT=8069
DB='db11-12'
USER='admin'
PASS='BLUE'
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
        cont = 1
        
        """ Fields """
        all_id = object_proxy.execute(DB,uid,PASS,'product.supplierinfo','search',[])
        for id in all_id:
            print(cont)
            object_proxy.execute_kw(DB,uid,PASS, 'product.supplierinfo', 'unlink', [[id]])
            cont += 1



def main():
    print("Ha comenzado el proceso")
    _create(True)
    print('Ha finalizado la carga tabla')
main()
