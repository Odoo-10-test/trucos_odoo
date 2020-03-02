# rsync

El comando linux rsync es una herramienta rápida y muy versátil para copiar archivos de forma local o remota. Así se describe este comando cuando ves la ayuda del comando man respecto al comando rsync. Este comando permite realizar una copia exacta de un archivo o directorio, en este último caso incluyendo todos los elementos dentro de este directorio, incluyendo todas las rutas y archivos, incluidos sus permisos y propiedades.

Una de las ventajas mas interesantes de este comando es que puede comprobar las dos rutas y actualizar solo los archivos nuevos y los que han cambiado de una ruta a otra. Si se interrumpiera el comando antes de concluir, solo basta con ejecutar de nuevo el comando y detectará cuales archivos faltaron para continuar donde se interrumpió.

```
rsync -avt *.sql root@157.230.8.181:/root
```

```
rsync --info=progress2 -e "ssh -i fu.pem" ubuntu@ec2-52-14-123-58.us-east-2.compute.amazonaws.com:/opt/odoo/backups/06_13_2019_01_49_55_1le.zip .
```

# subiendo
```
rsync --info=progress2 revisar_clientes.py  root@167.12.93.111:/opt/odoo/revisar_clientes.py
```

# Subiendo con Puerto
```
rsync --info=progress2 clientes.py -e "ssh -p 61022" root@server.okitup.net:/opt/odoo/clientes.py
```

