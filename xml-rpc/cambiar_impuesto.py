# -- coding: utf-8 --
#************#
# Importación Clientes y Proveedores #
#************#

import os
import csv
import xmlrpclib
import re


HOST='34.203.209.230'
PORT=8069
DB='aloprint'
USER='admin'
PASS='aloprintodoo123'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def _update_mass(estado):
    cont = 1
    product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('active','=',True)])
    if product:
        do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write',product, {'taxes_id':[(6, 0, [5])]})

def __main__():
    print 'Ha comenzado el proceso'
    _update_mass(True)
    print 'Ha finalizado la carga tabla'
__main__()
