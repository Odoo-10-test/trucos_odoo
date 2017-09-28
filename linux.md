# Mostrar espacio en disco
```
df -h
```

# Permisos Administrativos
```
sudo su
```

# Cambiar pass root
```
passwd
```

# Borrar todo el contenido de un directorio en Linux
```
sudo rm -R carpeta
```

# Actualizamos una base de datos de odoo

## paramos el proceso
```
/etc/init.d/odoo stop
```
## Actualizamos todo
```
su - odoo -s /bin/bash
python /opt/odoo/server/odoo-bin -c /etc/odoo/odoo.conf -d test -u all
```
## Iniciamos
```
/etc/init.d/odoo restart
```
