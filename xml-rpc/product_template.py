# -- coding: utf-8 --
#************#
# Importación Clientes y Proveedores #
#************#

import os
import csv
import xmlrpclib
import re


HOST='127.0.01'
PORT=8069
DB='elecmin-erp'
USER='admin'
PASS='pass'
path_file = 'productos.csv'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)



common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

# archive = csv.DictReader(open(path_file))

def _create(estado):
    if estado is True:
        archive = csv.DictReader(open(path_file))
        cont = 1
        name_anterior = ""

        for field in archive:
            cont += 1


            codigo = field['Cod. Producto'].strip()

            if codigo[-2:] != "US" or codigo[-2:] != "EU":
                nombre = field['Descripcion'].strip()
                print str(cont) + "--"+codigo +"---" + nombre

                producto = object_proxy.execute(DB,uid,PASS,'product.template','search',[('name','=',nombre)])
                producto_id = producto and producto[0]
                vals = {}
                if not producto_id:
                    vals['default_code'] = field['Cod. Producto'].strip()
                    vals['name'] = field['Descripcion'].strip()
                    vals['list_price'] = field['Precio Venta Neto'].strip().replace("$","").replace(".00","").replace(",","").replace("\n","")

                    product_id = object_proxy.execute(DB,uid,PASS,'product.template','create',vals)


            """

            producto_id = producto and producto[0]
            vals = {}
            if not producto_id:
                vals['name'] = field['Descripcion'].strip()

                print field['Descripcion'].strip()



                precio = field['PVP con Iva'].replace(",", '.').strip()
                vals['list_price'] = precio


                costo = field['Precio de costo'].replace(",", '.').strip()
                vals['standard_price'] = costo

                # Brand
                if field['Brand/Brand Name']:
                    vals1 = field['Brand/Brand Name'].strip()
                    brand = object_proxy.execute(DB,uid,PASS,'product.brand','search',[('name','=',vals1)])
                    brand_id = brand and brand[0]
                    vals['product_brand_id'] = brand_id

                # Dimensiones
                vals['product_ancho'] = field['Alto (cm)'].replace(",", '.').strip()
                vals['product_largo'] = field['Largo (cm)'].replace(",", '.').strip()
                vals['product_espesor'] = field['Alto (cm)'].replace(",", '.').strip()

                # Peso
                vals['weight'] = field['Peso (grs)'].replace(",", '.').strip()

                # Producto Almacenable
                vals['type'] = "product"


                print str(cont) + "= Inserto ==" + field['Nombre  NUEVO']

                partner_id = object_proxy.execute(DB,uid,PASS,'product.template','create',vals)
            else:
                print str(cont) + "= No Inserto ==" + field['Nombre  NUEVO']

            cont = cont + 1
            """





            """

            vals['default_code'] = field[' Código ']


            if field['Precio Lista'] == ' - ':
                vals['list_price'] = 0
            else:
                vals['list_price'] = field['Precio Lista'].replace(".", '')

            if field['Costo Producto'] == ' - ':
                vals['standard_price'] = 0
            else:
                vals['standard_price'] = field['Costo Producto'].replace(",", '')

            vals['largo'] = field['Largo']
            vals['weight'] = field['Nuevo Peso'].replace(",", '.')
            if field['Origen']:
                if field['Origen'] == ' PTI ' or field['Origen'] == 'PTI':
                    vals['sale_ok'] = True
                    vals['purchase_ok'] = False
                    vals['mat_type'] = 'PTI'
                else:
                    vals['sale_ok'] = True
                    vals['purchase_ok'] = True
                    vals['mat_type'] = 'PTE'
            # Cargando Familia
            if field['Familia']:
                vals1 = field['Familia'].strip()
                familia = object_proxy.execute(DB,uid,PASS,'product.family','search',[('name','=',vals1)])
                familia_id = familia and familia[0]
                vals['product_family_id'] = familia_id

            # Cargando Área
            if field['Area']:
                vals2 = field['Area'].strip()
                area = object_proxy.execute(DB,uid,PASS,'product.area','search',[('name','=',vals2)])
                area_id = area and area[0]
                vals['product_area_id'] = area_id

            # Cargando Línea
            if field['Linea']:
                vals3 = field['Linea'].strip()
                linea = object_proxy.execute(DB,uid,PASS,'product.linea','search',[('name','=',vals3)])
                linea_id = linea and linea[0]
                vals['product_linea_id'] = linea_id


            # Cargando Grupo
            if field['Grupo Producto']:
                vals4 = field['Grupo Producto'].strip()
                grupo = object_proxy.execute(DB,uid,PASS,'product.grupo','search',[('name','=',vals4)])
                grupo_id = grupo and grupo[0]
                vals['product_grupo_id'] = grupo_id


            # Cargando Sub Grupo
            if field['Sub Grupo Producto']:
                vals5 = field['Sub Grupo Producto'].strip()
                sgrupo = object_proxy.execute(DB,uid,PASS,'product.sgrupo','search',[('name','=',vals5)])
                sgrupo_id = sgrupo and sgrupo[0]
                vals['product_sgrupo_id'] = sgrupo_id

            # Cargando Familia
            if field['  Familia Material  ']:
                vals6 = field['  Familia Material  '].strip()
                familia = object_proxy.execute(DB,uid,PASS,'product.mfamily','search',[('name','=',vals6)])
                familia_id = familia and familia[0]
                vals['product_mfamily_id'] = familia_id


            # Categoría del Material
            if field['  Categoría Material  ']:
                vals7 = field['  Categoría Material  '].strip()
                categoria = object_proxy.execute(DB,uid,PASS,'product.categoria.material','search',[('name','=',vals7)])
                categoria_id = categoria and categoria[0]
                vals['product_categoria_material_id'] = categoria_id

            """




def main():
    print 'Ha comenzado el proceso'
    _create(True)
    print 'Ha finalizado la carga tabla'
main()





