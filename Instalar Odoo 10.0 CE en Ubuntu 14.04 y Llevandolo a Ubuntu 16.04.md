Hola en esta entrada veremos el paso a paso de como instalar Odoo 10 CE

1- Actualizamos de la versión 14.04 a la 16
```
sudo apt-get update

sudo apt-get upgrade

sudo apt-get dist-upgrade

sudo apt-get install update-manager-core

sudo do-release-upgrade
```
2- Actualizamos el sistema
```
 apt-get update &amp;&amp; apt-get upgrade
 ```
3- Creamos el usuario Odoo
```
 adduser --system --home=/opt/odoo --group odoo
 ```
4- Instalación de PostgreSQL

creamos el archivo pgdg.list
```
 nano /etc/apt/sources.list.d/pgdg.list
 ```
5- insertamos el siguiente código
```
 deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main
 ```
6- Importamos la llave del repositorio anterior, actualizamos e instalamos postgresql
```
 wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
sudo apt-get update
apt-get install postgresql postgresql-server-dev-9.6
```
7- Reiniciamos postgres, iniciamos sesión en postgres y creamos el usuario postgres
```
 service postgresql restart
su - postgres
createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo
```
8- Luego de ingresar la clave, salimos de la sesión de postgres
```
 exit
 ```
9- Descargamos Odoo, Instalamos unzip
```
 apt-get install unzip
 ```
10- Ingresamos en la carpeta /opt/odoo y descargamos la fuente para la versión comunity
```
 cd /opt/odoo/
wget https://github.com/odoo/odoo/archive/10.0.zip
unzip 10.0.zip
```
11- Renombramos la carpeta odoo-10.0 a server y le damos permisos al usuario odoo sobre esa carpeta
```
 mv odoo-10.0 server
chown -R odoo: server
```
12- Instalación de librerias, actualizamos pip e instalamos dependencias python de Odoo
```
 apt install python-pip libcups2-dev python-ldap libxml2-dev libxslt-dev node-less libsasl2-dev libldap2-dev python-lxml
pip install --upgrade pip
pip install -r /opt/odoo/server/requirements.txt
```
13- Creando un directorio para almacenar el archivo de logs
```
 mkdir /var/log/odoo/
chown odoo:root /var/log/odoo
```
14- Configurando Odoo Server
```
 mkdir /etc/odoo
cp /opt/odoo/server/debian/odoo.conf /etc/odoo/odoo.conf
chown odoo: /etc/odoo/odoo.conf
chmod 640 /etc/odoo/odoo.conf
```
15- Creamos la carpeta de los ExtraAddons
```
 mkdir /opt/odoo/server/extra-addons
chown odoo: /opt/odoo/ -R
```
16- Editamos el archivo odoo.conf
```
 nano /etc/odoo/odoo.conf
 ```
17- Modificamos y/o agregamos lo siguiente y guardamos el archivo, si no tienes módulo en estra-addons no coloque la ruta sino te dará problemas.
```
 db_user = odoo
db_password = CLAVE DEL USUARIO  ODOO EN POSTGRES
addons_path = /opt/odoo/server/addons,/opt/odoo/server/extra-addons
logfile = /var/log/odoo/odoo-server.log
```
18- Script de inicio automático de Odoo-Server en Ubuntu 16
```
 cp /opt/odoo/server/debian/init /etc/init.d/odoo
chmod 755 /etc/init.d/odoo
chown root: /etc/init.d/odoo
```
19-  Editamos el archivo:
```
 nano /etc/init.d/odoo
 ```
*Modificamos los siguientes valores, y guardamos el archivo:
```
 DAEMON=/opt/odoo/server/odoo-bin
 ```
20- Haciendo que Odoo se inicie automáticamente cuando reiniciemos nuestro servidor:
```
 update-rc.d odoo defaults
 ```
20a -  Haciendo que Postgresql se inicie automáticamente cuando reiniciemos nuestro servidor :
```
 update-rc.d postgresql enable
 ```
21-  Manipulamos el servicio
```
 /etc/init.d/odoo start|stop|restart
 ```
22- Editar archivo de configuración de postgres pg_hba.conf
```
 nano /etc/postgresql/9.6/main/pg_hba.conf
 ```
Editamos la siguiente linea
```
 local   all             all        peer

*Sustituimos por:

local   all             all       trust

```
23- Reiniciamos servicio de postgresql y odoo
```
 service postgresql restart
/etc/init.d/odoo restart
```
24- Instalar Libreria wkhtmltopdf
```
 sudo apt-get -f install
sudo apt-get install libxrender1 fontconfig xvfb libjpeg-turbo8
cd /opt
sudo wget http://download.gna.org/wkhtmltopdf/0.12/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb
sudo dpkg -i wkhtmltox-0.12.1_linux-trusty-amd64.deb
sudo cp /usr/local/bin/wkhtmltoimage /usr/bin/wkhtmltoimage
sudo cp /usr/local/bin/wkhtmltopdf /usr/bin/wkhtmltopdf
```
25- Reiniciamos
```
 /etc/init.d/odoo restart
 ```
26- Vemos el Log
```
 tail -f /var/log/odoo/odoo-server.log
 ```
27- Actualizamos la Zona horaria desde la consola de ubuntu
```
 tzselect
 ```
28 - Actualizamos la hora
```
 date --set "2007-05-27 17:27"
hwclock --set --date="2007-05-27 17:27"
hwclock
date
```
29- Por seguridad le ponemos un pass a Postgre
```
 sudo -u postgres psql postgres
\password postgres
Enter new password:
```
&nbsp;

Hasta aquí la instalación.... los siguientes comandos son para configuración de programación y no son necesarios.

K1 - revision de version 8
```
 /etc/init.d/o +Tab
/etc/init.d/odoov8 restart
tail -f /var/log/odoo/odoo-server.log
```
Otros Comando Importante

k2- Actualizar pass de Postgres
```
 sudo -su postgres
psql
alter role odoo with password 'odoo';
```
k3- Filtrar por base de datos en el fichero conf
```
 dbfilter = db10_*
 ```
k4 Configuracion de PyCharm

```
 /home/marlon/odoo/odoo_10/odoo-bin
--config=/home/marlon/odoo/odoo_10/odoo.conf
/home/marlon/odoo/odoo_10
```
k5 - Actualizar pass de una carpeta
```
 sudo chown marlon: -R odoo_10/
 ```
K6

/home/marlon/odoo/odoo_10/odoo.conf
```
 [options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = /home/marlon/odoo/odoo_10/addons
```
K7 - Descargando Odoo
```
 git clone https://github.com/odoo/odoo.git --branch 10.0 --single-branch odoo_10
 ```
K8 - Configuracion de Pycharm
```
 /home/marlon/Documentos/odoo-apt/odoo-10.0/odoo-bin
 ```
```
 --config=/home/marlon/Documentos/odoo-apt/odoo-10.0/debian/odoo.conf
 ```
K9 - Acceso SSH con un fichero ppk
```
>sudo apt-get install putty
puttygen <span class="skimlinks-unlinked">private.ppk</span> -o private-key -O private-openssh
ssh -i private-key username@remote-server-ip
```
