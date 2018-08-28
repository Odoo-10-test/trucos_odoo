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
https://www.facebook.com/PromoPrint-Impresi%C3%B3n-Digital-1941563209434712/
rsync -e "ssh -i odoo.pem" ubuntu@ec2-11-219-12-21.us-east-2.compute.amazonaws.com:/home/ubuntu/cron-odoo/cron-backup/127.0.0.1_db10-chile-sii_20180525_0044973862841.sql.gz /home/marlon/MEGA/CLIENTES/MARYUN/AWS
```
