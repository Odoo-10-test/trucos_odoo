# -- coding: utf-8 --
#************#
# Importación Clientes y Proveedores #
#************#

import os
import csv
import xmlrpclib
import re


HOST='127.0.0.1'
PORT=8069
DB='db10-chile-sii'
USER='admin'
PASS='x1234567890'
path_file = 'email.csv'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def _update_mass(estado):
    cont = 1
    partner = object_proxy.execute(DB,uid,PASS,'res.partner','search',[('active','=',True)])

    for field in partner:
        if partner:
            partner = object_proxy.execute(DB,uid,PASS,'res.partner','read',[field],[])
            rut = partner[0]['document_number']
            idf = partner[0]['id']
            if rut:
                cont = cont + 1
                archive = csv.DictReader(open(path_file))
                for field in archive:
                    rut_csv = field['Rut Beneficiario']
                    int_rut = rut_csv.replace(".", '').replace("-", '')
                    rut = rut.replace(".", '').replace("-", '')

                    if int_rut == rut:
                        print int_rut
                        print rut
                        print "MACH"
                        email = field['Email']
                        vals = {}
                        vals['dte_payment'] = email

                        # do_write = object_proxy.execute(DB,uid,PASS,'res.partner', 'write',field, {'dte_payment':email})
                        do_write = object_proxy.execute(DB,uid,PASS,'res.partner', 'write', idf, vals)


                print str(cont) + "-->" +str(rut)



        """

         """



def __main__():
    print 'Ha comenzado el proceso'
    _update_mass(True)
    print 'Ha finalizado la carga tabla'
__main__()






