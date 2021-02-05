# -- coding: utf-8 --
#************#
import os
import csv
import xmlrpclib
import re

HOST='127.0.0.1'
PORT=8069
DB='db13-spain'
USER='admin'
PASS='x1234567890'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def _update_mass(estado):
    cont = 1
    product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('active','=',True)])
    print(product)

def __main__():
    print 'Ha comenzado el proceso'
    _update_mass(True)
    print 'Ha finalizado la carga tabla'
__main__()
