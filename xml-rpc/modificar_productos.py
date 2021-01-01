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
DB='db11-spain'
USER='admin'
PASS='idonothavepass'
path_file = 'product.csv'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)


def _create(estado):
    if estado is True:
        cont = 0
        product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('active','=',True)])
        for field in product:
            cont += 1
            product_obj = object_proxy.execute(DB,uid,PASS,'product.template','read',[field],[])
            
            width = product_obj[0]['width']
            length = product_obj[0]['length']
            height = product_obj[0]['height']
            volume = product_obj[0]['volume']

            do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write',field, 
                {
                    'width':0, 
                    'length':0,
                    'height':0,
                    'volume':0,

                    'package_width':width, 
                    'package_length':length,
                    'package_height':height,
                    'package_volume':volume,
                },
            )

            print(cont)
            print(product_obj[0]['name'])


def main():
    print("Ha comenzado el proceso")
    _create(True)
    print('Ha finalizado la carga tabla')
main()
