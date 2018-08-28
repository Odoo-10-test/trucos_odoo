# Consultas rápidas a Odoo

# Filtrando por subdominio
```
dbfilter = ^%d$
```


# Filtrando por dominio
```
dbfilter = ^%h$
```

# Descargamos la bd

```
rsync --info=progress2 -e "ssh -i odoo.pem" ubuntu@ec2-18-212-135-201.us-east-2.compute.amazonaws.com:/opt/odoo/backups/27_08_2018_03_55_01_db10-chile-sii.zip /home/marlon/MEGA/CLIENTES/AZUL/AWS
```

# Parar Proceso

```
ps aux | grep server
kill -9 20026
```
# Borrar Logs

```
para saber si es el log lo que mas pesa, usas
du -hs
cd /var/log/odoo
rm odoo-server.log
```
