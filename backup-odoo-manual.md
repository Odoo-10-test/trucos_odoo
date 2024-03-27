# Describo los pasos para hacer respaldo en Odoo de forma manual

1. Hacemos un respaldo de la base de datos en el servidor de origen
```
pg_dump -U odoo -h localhost -p 5432 basedatos > basedatos.dump
```

2. Respaldamos los filestore
```
zip -r filestore-basedatos.zip /opt/odoo/.local/share/Odoo/filestore/basedatos
```
   

3. Montamos el respaldo
```
sudo -u postgres psql
CREATE DATABASE nueva_base_de_datos WITH OWNER = odoo;
```
