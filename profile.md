


# Actualizar con Pull
```
odoo_actualizar(){
  echo Deteniendo Odoo
  /etc/init.d/odoo stop
  for i in /opt/odoo/server/extra-addons/*
  do
    echo Actualizando $i
    git -C $i pull
  done
  if [[ ! -z "$1" ]]; then
    echo "Actualizando server odoo"
    sudo -u odoo python /opt/odoo/server/odoo-bin -c /etc/odoo/odoo.conf -d $1 -u all --stop-after-init
  fi
  /etc/init.d/odoo start
  echo Finalizado
}
```

# Reiniciamos Odoo

```
/root/.profile
source .profile
```

# Actualizar
```
actualizar(){
  for i in /home/marlon/Documents/odoo-10.0/extra-addons/*
  do
    echo Actualizando $i
    git -C $i pull
  done
  echo Finalizado
}
```

# Borrando los .pyc
```
rm **/**/*.pyc
rm **/*.pyc
```



