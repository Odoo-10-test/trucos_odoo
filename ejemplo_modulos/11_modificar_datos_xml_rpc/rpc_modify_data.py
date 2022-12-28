# -- coding: utf-8 --
#************#
# Create
#************#

import xmlrpc.client
import csv

host = '127.0.0.1'
port = 8069
db = 'db16-other'
user = 'admin'
password = 'x1234567890'

url = 'http://%s:%d/xmlrpc/2/' % (host, port)

common_proxy = xmlrpc.client.ServerProxy(url + 'common')
object_proxy = xmlrpc.client.ServerProxy(url + 'object')
uid = common_proxy.login(db, user, password)
if uid:
    print('Conectado al servidor maestro')

def _create(state):
    print("=1=")
    print(state)
    if state is True:
        archive = csv.DictReader(open('data.csv'))
        cont = 0
        for field in archive:
            cont += 1
            _name = field['name'].strip()
            _email = field['email'].strip()
            _phone = field['phone'].strip()

            vals = {}
            vals['email'] = _email
            vals['phone'] = _phone
            print(vals)

            # Validate the register does not exist
            _id = object_proxy.execute_kw(db, uid, password, 'res.partner', 'search', [[['name', '=', _name]]])
            if _id:
                _partner = object_proxy.execute(db, uid, password, 'res.partner' ,'write',_id , vals)
                if _partner:
                    print("Se ha modificado el registro: ")
                else:
                    print("No se ha modificado el registro: ")
            else:
                print('= El registro no existe =')
                
            
        cont += 1
        print("Se han modificado: ", cont)


def main():
    print("Ha comenzado el proceso")
    _create(True)
    print('Ha finalizado la carga tabla')
main()