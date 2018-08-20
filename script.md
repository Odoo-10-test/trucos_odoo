# Carga de Datos
```
import os
import csv
import xmlrpclib
import re


HOST='127.0.0.1'
PORT=8069
DB='db10-chile-sii-arquipunto-local'
USER='admin'
PASS='xarquipunto'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def html_escape(text):
    """Produce entities within text."""
    html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }
    return "".join(html_escape_table.get(c,c) for c in text)


def _update(estado):

    if estado is True:
        path_file = 'productos2.csv'
        archive = csv.DictReader(open(path_file))
        contador = 1
        a = []
        for field in archive:
            name = html_escape(field["Nombre  NUEVO"].replace('"', '').replace("'", '').strip())
            name = field["Nombre  NUEVO"].strip()

            producto = object_proxy.execute(DB,uid,PASS,'product.template','search',[('name','=',name)])
            producto_id = producto and producto[0]
            if not producto_id:
                print "es nuevo"

            # Buscamos el Id del producto a actualizar
            product_tmpl_id = object_proxy.execute(DB,uid,PASS,'product.template','search',[('name','=',name)])
            if not product_tmpl_id:
                print "No conseguido:" + name + ":"
            else:
                # Insertamos cantidad de hojas
                value_color = html_escape(field["Cantidad de hojas "].replace('"', '').replace("'", '').strip())
                if value_color:
                    cadena = "Cantidad de hojas"+value_color
                    if not cadena in a:
                        a.append(cadena)
                        print "aaaaaaaaaaaaaaaa"
                        print a


                        if value_color and product_tmpl_id:
                            contador = contador + 1
                            value_color_ids = object_proxy.execute(DB,uid,PASS,'product.attribute.value','search',[('name','=',value_color)])
                            attribute_color = object_proxy.execute(DB,uid,PASS,'product.attribute.value','read',value_color_ids,['attribute_id','name'])

                            # Insertamos el atributo

                            print "--------------------------"
                            print attribute_color
                            if value_color:
                                print contador
                                print '* Creando atributo Color con valor:',attribute_color[0]['name']
                                vals={'product_tmpl_id': product_tmpl_id[0],'attribute_id':attribute_color[0]['attribute_id'][0], 'value_ids': [(6,0,value_color_ids)]}

                                print vals
                                line = object_proxy.execute(DB,uid,PASS,'product.attribute.line','create',vals)
                                print  "Para el producto: %r" % ( object_proxy.execute(DB,uid,PASS,'product.attribute.line','read',[line],['product_tmpl_id'])[0]['product_tmpl_id'][1])



def __main__():
    print 'Ha comenzado el proceso'
    _update(True)
    print 'Ha finalizado la carga tabla'
__main__()
```
