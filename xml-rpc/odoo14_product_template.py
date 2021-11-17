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


if uid:
    print('Conectado al servidor maestro')
