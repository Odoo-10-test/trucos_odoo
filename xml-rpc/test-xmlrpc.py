# -- coding: utf-8 --
#************#
# Importación Clientes y Proveedores #
#************#

import xmlrpclib

HOST='127.0.0.1'
PORT=8069
DB='db10-chile-sii'
USER='admin'
PASS='x1234567890'

url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)



# archive = csv.DictReader(open(path_file))

def _create(estado):
    if uid:
        print("Conectado")
    else:
        print("No Conectado" )

def main():
    print 'Ha comenzado el proceso'
    _create(True)
    print 'Ha finalizado la carga tabla'
main()





