# -*- coding: utf-8 -*-
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import re
from datetime import datetime


print "#################################################################"
print "# Creación de archivos data                                     #"
print "# www.ynext.cl                                                  #"
print "# Autor: Marlon Falcon Herandez                                 #"
print "# mail: mfalcon@ynext.cl                                        #"
print "#################################################################"


modelo = 'product.sgrupo'
namet = modelo.replace(".", '_')
file_name_fuente = namet + '.csv'
file_name_data = namet + '_data.xml'

# file_name_fuente = 'rubro.csv'
# file_name_data = 'partner_rubro_data.xml'

path_file = file_name_fuente
archive = csv.DictReader(open(path_file))
cont = 1
print 'La creación Fichero a Iniciado'

file = open(file_name_data,'w')
file.write('<?xml version="1.0" encoding="utf-8"?> \n')
file.write('<odoo> \n')
file.write('    <data noupdate="1">\n')


for field in archive:
            file.write('       <record id="SGB'+ str(cont) +'" model="'+modelo+'">\n')
            file.write('           <field name="name">'+ field['Sub Grupo']+'</field>\n')
            file.write('       </record>\n')
            cont = cont + 1
            print cont
file.write('    </data>\n')
file.write('</odoo> \n')
file.close()

print 'Ha finalizado la creación Fichero'
