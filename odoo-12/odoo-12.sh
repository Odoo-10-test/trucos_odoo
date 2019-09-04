#!/bin/bash
#
# Author: Sherif Khaled
# Copyright (c) 2019.
#
# This program is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free Software
# Foundation; either version 3.0 of the License, or (at your option) any later
# version.
#
# This install-odoo.sh will install and configure the odoo system, without user interaction with the script
# steps at
#    https://www.odoo.com/documentation/10.0/setup/install.html
#
# Examples:-
# Install odoo version 10 and configure using server external IP address
# .\install-odoo.sh -v 10
#
# Install odoo version 10 and configure using hostname odoo.example.com
# .\install-odoo.sh -v 10 -S odoo.example.com
#
# Install odoo version 10 with a SSL certificate from Let's Encrypt using e-mail info@example.com:
# .\install-odoo.sh -v 10 -S odoo.example.com -M info@example.com
#
# Install odoo version 10 with specific port 8070
# .\install-odoo.sh -v 10 -S odoo.example.com -M info@example.com -r 8070
#
# Install odoo version 10 with postgres password and Master password
# .\install-odoo.sh -v 10 -S odoo.example.com -M info@example.com -r 8070 -p sql123 -a admin123
#
# Note: this script tested on ubuntu 16.4.
#

USAGE(){
  cat 1>&2 <<HERE
  Installer script for setting up odoo system.
  This script support odoo Version (10 ,11 ,12), also this script
  supports installation on cloud host or localhost.
  USAGE:
      odoo-install.sh [OPTIONS]
  OPTIONS (Install odoo system):
      -v    <version>        Install given version of odoo (e.g. '10.0') [required]
      -e    <is enterprise>  chose if odoo is enterprise                 [optional]
      -a    <admin password> Password for odoo administrator             [recommended]
      -p    <sql password>   setup password for postgresql               [recommended]
      -r    <server port>    spsifec server port,default port 8069       [optional]
      -w    <wkhtmltopdf>    install wkhtmltopdf pachage.                [optional]
      -s    <nginx/apache>   select the server type,default nginx server [optional]
      -h                     Print help
  OPTIONS (support SSL)
      -S    <hostname>       Configure server with <hostname> [required]
      -M    <email>          E-mail for Let's Encrypt certbot [required]
      -K    <RSA Size>       Select SSL RSA Size 2048/4069 bit,default 2048 bit RSA [optional]
  EXAMPLES
     setup odoo system
        .\install-odoo.sh -v 10
        .\install-odoo.sh -v 10 -S odoo.example.com -a 123
        .\install-odoo.sh -v 10 -S odoo.example.com -M info@example.com -a 123 -p sql123
        .\install-odoo.sh -v 10 -S odoo.example.com -M info@example.com -a 123 -p sql123 -r 8069
  SUPPORT:
      Source: https://github.com/Sherif-khaled/install-odoo
      Commnity: https://odoo-community.org/
HERE
}

main(){

 check_x64
 check_mem
 #check_ubuntu 16.04

# Default Parameters
 get_ip
 HOST=$EXTERNAL_IP
 PORT=8069
 IS_ENTERPRISE=false
 INSTALL_WKHTMLTOPDF=false
 SERVER_TYPE="nginx"
 RSA_DH_SIZE=2048

  while builtin getopts "hv:a:p:r:s:S:M:K:ew" opt "${@}"; do
    case $opt in
      h)
        USAGE
        exit 0
        ;;

      v)
        VERSION=$OPTARG
        check_version $VERSION
        ;;
      e)
        IS_ENTERPRISE=true
        ;;
      a)
        PASS=$OPTARG
        check_admin_pass $PASS
        ;;
      p)
        SQL_PASS=$OPTARG
        check_sql_pass $SQL_PASS
        ;;
      r)
        PORT=$OPTARG
        check_port $PORT
        ;;
      w)
        INSTALL_WKHTMLTOPDF=true
        ;;
      s)
        SERVER=$OPTARG
        check_server_type $SERVER
        ;;
      S)
        HOST=$OPTARG
        check_host $HOST
        ;;
      M)
        EMAIL=$OPTARG
        check_email $EMAIL
        ;;
      K)
        RSA_DH_SIZE=$OPTARG
        check_rsa_size $RSA_DH_SIZE
        ;;
      :)
        err "Missing option argument for -$OPTARG"
        exit 1
        ;;
      \?)
        err "Invalid option: -$OPTARG" >&2
        USAGE
        ;;
    esac
  done
install_odoo
}


# Check root privilege,the script required root privilege to make all configurations
check_root() {
  if [ $EUID != 0 ]; then err "You must run this script as root."; fi
}
#generate script errors
err(){
  echo "install-odoo.sh say: $1"
  exit 1
}
# check odoo versions if supported or not.
check_version(){
  ver=$1
  case $ver in
    10)
       return $ver
      ;;
    11)
       return $ver
      ;;
    12 )
       return $ver
      ;;
    *)
       err "the script not supported this version $ver"
  esac

}
# check odoo admin master password if null value
check_admin_pass(){
  if [ -z $1 ];then
    err "please enter the admin password"
  fi
}
# check odoo postgresql user password if null value
check_sql_pass(){
  if [ -z $1 ];then
    err "please enter the postgresql password"
  fi
}
# check port value if in supported range or not.
check_port(){
  re='^[0-9]+$'
  if ! [[ $1 =~ $re ]] ; then
	   err "the port value must be a number"	
  elif [ $1 -gt 8090 ] && [ $1 -lt 8060 ];then
       err "the port number must be between [8060] and [8090]"
  fi
}
check_host(){

  if [ -z $1 ];then
    err "please enter your hostname"
  fi

  DIG_IP=$(dig +short $1 | grep '^[.0-9]*$' | tail -n1)

  get_ip
  if [ -z "$DIG_IP" ]; then err "Unable to resolve $1 to an IP address using DNS lookup."; fi

  if [ "$DIG_IP" != "$EXTERNAL_IP" ]; then err "DNS lookup for $1 resolved to $DIG_IP but didn't match local $EXTERNAL_IP."; fi
}
get_ip(){
  apt update
  apt install dnsutils
  EXTERNAL_IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"
}
check_email(){
  if [ -z $1 ];then
    err "please enter your email"
  fi
}
check_rsa_size(){
  size=$1
  case $size in
    2048)
       return $size
      ;;
    4096)
       return $size
      ;;
    *)
       err "the script not supported this RSA size $size"
  esac
}
check_mem() {
  MEM=`grep MemTotal /proc/meminfo | awk '{print $2}'`
  MEM=$((MEM/1000))
  if (( $MEM < 2048 )); then err "Your server needs to have (at least) 2G of memory."; fi
}

check_ubuntu(){
  RELEASE=$(lsb_release -r | sed 's/^[^0-9]*//g')
  if [ "$RELEASE" != $1 ]; then err "You must run this command on Ubuntu $1 server."; fi
}

check_x64() {
  UNAME=`uname -m`
  if [ "$UNAME" != "x86_64" ]; then err "You must run this command on a 64-bit server."; fi
}
#Check apache/nginx server
check_server_type() {

  if [ $1 == "nginx" ];then
    if dpkg -l | grep -q apache2; then
      apt-get purge apache2
      apt-get auto-remove
    fi
  elif [ $1 == "apache" ] || [ $1 == "apache2" ];then
    if dpkg -l | grep -q apache2; then
      apt-get purge nginx
      apt-get auto-remove
    fi
  else
    err "you select unsupported server, or uncorrected spelling [apache2/nginx]"
  fi
}
# Update repositories,and upgrade system
upgrade_system(){
  echo -e "\n---- Update Server ----"
  apt update
  apt dist-upgrade -y
}
# configure and allow ports in UFW firewall
configure_ufw(){
  service ufw start
  ufw allow ssh       # allow ssh port
  ufw allow $PORT/tcp # allow odoo port
  ufw allow 8072/tcp  # allow longpolling port
  ufw allow 80/tcp    # allow http port

  if [ ! -z $EMAIL ];then
  	ufw allow 443/tcp # allow https port
  fi
  echo "y" | ufw enable $answer
}
#Install all dependencies
install_dependencies(){

  declare -a dependencies=("git" "postgresql" "postgresql-server-dev-9.5" "libzip-dev"
                           "libxml2-dev" "build-essential" "wget" "libxslt-dev" "libldap2-dev"
                           "libxslt1-dev" "libsasl2-dev" "libldap2-dev" "pkg-config" "libsasl2-dev"
                           "libtiff5-dev" "libjpeg8-dev" "libjpeg-dev" "zlib1g-dev" "node-less"
                           "libfreetype6-dev" "liblcms2-dev" "liblcms2-utils" "libwebp-dev"
                           "tcl8.6-dev" "tk8.6-dev" "libyaml-dev" "fontconfig")

 declare -a python_env=("python-pip" "python-all-dev" "python-dev" "python-setuptools" "python-tk" "gevent" "psycogreen")

 declare -a python3_env=("python3-pip" "python3-software-properties" "python3-all-dev" "python3-dev"
                         "python3-setuptools" "python3-tk" "python3-venv" "python3-wheel" "python3-gevent")

 for (( i = 0; i < ${#dependencies[@]} ; i++ )); do
     printf "\n**** Basic dependencies installing now: ${dependencies[$i]} *****\n\n"

     # Run each command in array
     eval "apt-get install ${dependencies[$i]} -y"
 done

 if [ $VERSION -eq 10 ] || [ $VERSION -eq 9 ];then

   for (( i = 0; i < ${#python_env[@]} ; i++ )); do
       printf "\n**** python env installing now: ${python_env[$i]} *****\n\n"

       # Run each command in array
       eval "apt-get install ${python_env[$i]} -y"
   done

elif [ $VERSION -eq 12 ] || [ $VERSION -eq 11 ];then
  for (( i = 0; i < ${#python3_env[@]} ; i++ )); do
      printf "\n**** python3 env Installing now : ${python3_env[$i]} *****\n\n"

      # Run each command in array
      eval "apt-get install ${python3_env[$i]} -y"
  done
fi
}
# Create postgresql user and odoo user
create_user(){
  #create postgresql user
  sudo -u postgres -H -- psql -d postgres -c "CREATE USER odoo$VERSION WITH PASSWORD '$PASS'"
  sudo -u postgres -H -- psql -d postgres -c "ALTER USER odoo$VERSION WITH SUPERUSER;"
  #create odoo user
  adduser --system --home=/opt/odoo$VERSION --group odoo$VERSION
  adduser odoo$VERSION sudo

}
# create Logs Directory
configure_logs(){
  mkdir /var/log/odoo$VERSION
  chown odoo$VERSION:odoo$VERSION /var/log/odoo$VERSION
}
install_python_dependencies(){

  if [ $VERSION -eq 9 ] || [ $VERSION -eq 10 ];then
    #install python dependencies
    pip install -r /opt/odoo$VERSION/doc/requirements.txt
    pip install -r /opt/odoo$VERSION/requirements.txt
  elif [ $VERSION -eq 11 ] || [ $VERSION -eq 12 ];then
    #install python3 dependencies
    pip3 install -r /opt/odoo$VERSION/doc/requirements.txt
    pip3 install -r /opt/odoo$VERSION/requirements.txt
  fi

  #Install Less CSS via Node.js and npm
  curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
  apt install -y nodejs
  npm install -g less less-plugin-clean-css rtlcss

  #Install Wkhtmltopdf
  if [ $INSTALL_WKHTMLTOPDF = true ];then
    cd /tmp
    wget https://downloads.wkhtmltopdf.org/0.12/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb
    dpkg -i wkhtmltox-0.12.1_linux-trusty-amd64.deb
    ln -s /usr/local/bin/wkhtmltopdf /usr/bin
    ln -s /usr/local/bin/wkhtmltoimage /usr/bin
  fi
}
create_odoo_config(){
  echo "[options]" >> /etc/odoo$VERSION-server.conf
  echo "admin_passwd = $PASS" >> /etc/odoo$VERSION-server.conf
  echo "db_host = False" >> /etc/odoo$VERSION-server.conf
  echo "db_port = False" >> /etc/odoo$VERSION-server.conf
  echo "db_user = odoo$VERSION" >> /etc/odoo$VERSION-server.conf
  echo "db_password = False" >> /etc/odoo$VERSION-server.conf
  if [ $IS_ENTERPRISE = true ]; then
    echo "addons_path = /opt/odoo$VERSION/enterprise/addons" >> /etc/odoo$VERSION-server.conf
  else
    echo "addons_path = /opt/odoo$VERSION/addons" >> /etc/odoo$VERSION-server.conf
  fi
  echo "xmlrpc_interface = 127.0.0.1" >> /etc/odoo$VERSION-server.conf
  echo "netrpc_interface = 127.0.0.1" >> /etc/odoo$VERSION-server.conf
  echo ";xmlrpc_port = $PORT" >> /etc/odoo$VERSION-server.conf
}
create_odoo_service(){
  echo "[Unit]" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "Description=Odoo Open Source ERP and CRM" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "Requires=postgresql.service" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "After=network.target postgresql.service" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "[Service]" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "Type=simple" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "PermissionsStartOnly=true" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "SyslogIdentifier=odoo-server" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "User=odoo$VERSION" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "Group=odoo$VERSION" >> /lib/systemd/system/odoo$VERSION-server.service
  if [ $IS_ENTERPRISE = true ]; then
    echo "ExecStart=/opt/odoo$VERSION/odoo-bin --config=/etc/odoo$VERSION-server.conf --addons-path=/opt/odoo$VERSION/enterprise/addons/" >> /lib/systemd/system/odoo$VERSION-server.service
  else
    echo "ExecStart=/opt/odoo$VERSION/odoo-bin --config=/etc/odoo$VERSION-server.conf --addons-path=/opt/odoo$VERSION/addons/" >> /lib/systemd/system/odoo$VERSION-server.service
  fi
  echo "WorkingDirectory=/opt/odoo$VERSION/" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "StandardOutput=journal+console" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "[Install]" >> /lib/systemd/system/odoo$VERSION-server.service
  echo "WantedBy=multi-user.target" >> /lib/systemd/system/odoo$VERSION-server.service

}
odoo_configuration(){

  #Create Odoo configuration File
  create_odoo_config

  #Create an Odoo Service
  create_odoo_service

  #Change File Ownership and Permissions
  chmod 755 /lib/systemd/system/odoo$VERSION-server.service
  chown root: /lib/systemd/system/odoo$VERSION-server.service
  chown -R odoo$VERSION: /opt/odoo$VERSION/
  chown odoo$VERSION:root /var/log/odoo$VERSION
  chown odoo$VERSION: /etc/odoo$VERSION-server.conf
  chmod 640 /etc/odoo$VERSION-server.conf

}
server_configuration(){

  if [ $SERVER == "apache" ] || [ $SERVER == "apache2" ];then

    apt-get install apache2 -y
    a2enmod proxy proxy_http

    cat > /etc/apache2/sites-available/$HOST.conf << HERE
    <VirtualHost *:80>
      ServerName $HOST
      ServerAlias www.$HOST
      LogLevel warn
      ErrorLog /var/log/apache2/$HOST.error.log
      CustomLog /var/log/apache2/$HOST.access.log combined
      ProxyRequests Off
      <Proxy *>
        Order deny,allow
        Allow from all
      </Proxy>
      ProxyPass / http://$HOST:$PORT/
      ProxyPassReverse / http://$HOST:$PORT/
      <Location />
        Order allow,deny
        Allow from all
      </Location>
    </VirtualHost>
HERE

  a2dissite 000-default.conf
  a2ensite $HOST.conf
  systemctl restart apache2

  else
  apt-get install nginx -y
  systemctl enable nginx

  cat > /etc/nginx/sites-available/$HOST << HERE
  upstream odoo {
  server 127.0.0.1:$PORT;
  }
  server {
  listen 80;
  server_name $HOST;
  access_log /var/log/nginx/$HOST.access.log;
  error_log /var/log/nginx/$HOST.error.log;
  proxy_buffers 16 64k;
  proxy_buffer_size 128k;
  location / {
    proxy_pass http://odoo;
    proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
    proxy_redirect off;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
   }
  location /longpolling {
    proxy_pass http://127.0.0.1:8072;
   }
  location ~* /web/static/ {
    proxy_cache_valid 200 60m;
    proxy_buffering on;
    expires 864000;
    proxy_pass http://odoo;
   }
  }
HERE

ln -s /etc/nginx/sites-available/$HOST /etc/nginx/sites-enabled/$HOST
rm /etc/nginx/sites-enabled/default
systemctl restart nginx
fi

}
create_ssl_cert(){
  echo -n "\n" | add-apt-repository ppa:certbot/certbot
  apt-get update

  if [ $SERVER == "apache" ] || [ $SERVER == "apache2" ];then

  	apt-get install python-certbot-apache -y

  	mkdir /etc/apache2/ssl
  	openssl dhparam -out /etc/apache2/ssl/dhp-$RSA_DH_SIZE.pem $RSA_DH_SIZE
  	chmod 600 /etc/apache2/ssl/dhp-$RSA_DH_SIZE.pem

  	yes N | certbot --apache -d $HOST -d www.$HOST -m $EMAIL --agree-tos --redirect -n
    systemctl restart apache2

  else

  	apt-get install python-certbot-nginx -y

  	mkdir /etc/nginx/ssl
  	openssl dhparam -out /etc/nginx/ssl/dhp-$RSA_DH_SIZE.pem $RSA_DH_SIZE
  	chmod 600 /etc/nginx/ssl/dhp-$RSA_DH_SIZE.pem

    yes N | certbot --nginx -d $HOST -d www.$HOST -m $EMAIL --agree-tos --redirect -n
    systemctl restart nginx

  fi

}
configur_ssl_server(){

  if [ $SERVER == "apache" ] || [ $SERVER == "apache2" ];then
    cat > /etc/apache2/sites-available/$HOST.conf << HERE
  <VirtualHost *:80>
       ServerName $HOST
       ServerAlias $HOST
       Redirect / https://$HOST/
  </VirtualHost>
  <VirtualHost *:443>
       ServerName $HOST
       ServerAlias $HOST
       LogLevel warn
       ErrorLog /var/log/apache2/$HOST.error.log
       CustomLog /var/log/apache2/$HOST.access.log combined
       SSLEngine on
       SSLProxyEngine on
       SSLCertificateFile /etc/letsencrypt/live/$HOST/fullchain.pem
       SSLCertificateKeyFile /etc/letsencrypt/live/$HOST/privkey.pem
       ProxyPreserveHost On
       ProxyPass / http://127.0.0.1:$PORT/ retry=0
       ProxyPassReverse / http://127.0.0.1:$PORT/
  </VirtualHost>
  # modern configuration, tweak to your needs
  SSLProtocol             all -SSLv3 -TLSv1 -TLSv1.1
  SSLCipherSuite          ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256
  SSLOpenSSLConfCmd DHParameters /etc/apache2/ssl/dhp-$RSA_DH_SIZE.pem
  SSLHonorCipherOrder     on
  SSLCompression          off
  SSLSessionTickets       off
  # OCSP Stapling, only in httpd 2.3.3 and later
  SSLUseStapling          on
  SSLStaplingResponderTimeout 5
  SSLStaplingReturnResponderErrors off
  SSLStaplingCache        shmcb:/var/run/ocsp(128000)
HERE

a2enmod ssl proxy proxy_http
a2dissite 000-default.conf
a2ensite $HOST.conf
systemctl restart apache2
  else

  cat > /etc/nginx/sites-available/$HOST << HERE
# Odoo servers
upstream odoo {
 server 127.0.0.1:$PORT;
}
# HTTP -> HTTPS
server {
    listen 80;
    server_name www.$HOST $HOST;
}
server {
   listen 443 ssl http2;
   server_name $HOST;
   # certs sent to the client in SERVER HELLO are concatenated in ssl_certificate
   ssl_certificate /etc/letsencrypt/live/$HOST/fullchain.pem;
   ssl_certificate_key /etc/letsencrypt/live/$HOST/privkey.pem;
   ssl_session_timeout 10m;
   ssl_session_cache shared:SSL:10m;
   ssl_session_tickets off;
   ssl_protocols TLSv1.1 TLSv1.2;
   ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
   ssl_prefer_server_ciphers on;
   ssl_dhparam /etc/nginx/ssl/dhp-$RSA_DH_SIZE.pem;
   ssl_ecdh_curve secp384r1;
   # HSTS (ngx_http_headers_module is required) (15768000 seconds = 6 months)
   add_header Strict-Transport-Security max-age=15768000;
   # fetch OCSP records from URL in ssl_certificate and cache them
   ssl_stapling on;
   ssl_stapling_verify on;
   # verify chain of trust of OCSP response using Root CA and Intermediate certs
   ssl_trusted_certificate /etc/letsencrypt/live/$HOST/chain.pem;
   resolver 8.8.8.8 8.8.4.4;
   access_log /var/log/nginx/odoo$VERSION.access.log;
   error_log /var/log/nginx/odoo$VERSION.error.log;
   proxy_read_timeout 720s;
   proxy_connect_timeout 720s;
   proxy_send_timeout 720s;
   proxy_set_header X-Forwarded-Host \$host;
   proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto \$scheme;
   proxy_set_header X-Real-IP \$remote_addr;
   location / {
     proxy_redirect off;
     proxy_pass http://odoo;
   }
   location /longpolling {
     proxy_pass http://127.0.0.1:8072;
   }
   location ~* /web/static/ {
       proxy_cache_valid 200 90m;
       proxy_buffering    on;
       expires 864000;
       proxy_pass http://odoo;
   }
  # gzip
  gzip_types text/css text/less text/plain text/xml application/xml application/json application/javascript;
  gzip on;
}
HERE
ln -s /etc/nginx/sites-available/$HOST /etc/nginx/sites-enabled/$HOST
rm /etc/nginx/sites-enabled/default
systemctl restart nginx

fi
}
install_odoo(){
  upgrade_system
  configure_ufw
  install_dependencies
  create_user
  configure_logs
  git clone https://www.github.com/odoo/odoo --depth 1 --branch $VERSION.0 --single-branch /opt/odoo$VERSION
  if [ $IS_ENTERPRISE = true ];then

    # Odoo Enterprise install!

   ln -s /usr/bin/nodejs /usr/bin/node
   mkdir odoo$VERSION/enterprise
   mkdir odoo$VERSION/enterprise/addons

    GITHUB_RESPONSE=$(git clone --depth 1 --branch $VERSION.0 https://www.github.com/odoo/enterprise "/opt/odoo$VERSION/enterprise/addons" 2>&1)
    while [[ $GITHUB_RESPONSE == *"Authentication"* ]]; do
      ((count++))
        echo "------------------------WARNING------------------------------"
        echo "Your authentication with Github has failed! Please try again."
        printf "In order to clone and install the Odoo enterprise version you \nneed to be an offical Odoo partner and you need access to\nhttp://github.com/odoo/enterprise.\n"
        echo "TIP: Press ctrl+c to stop this script."
        echo "-------------------------------------------------------------"
        echo " $count attempt from 4 attempts "
        GITHUB_RESPONSE=$(sudo git clone --depth 1 --branch 12.0 https://www.github.com/odoo/enterprise "~/Desktop/enterprise/addons" 2>&1)
        if [ $count -eq 1 ];then
          echo "please check your github credentials and try again later."
          read -r -p "Do you want continue to configure server to using odoo community? [Y/N]" answer
          case $answer in [yY][eE][sS]|[yY])
          break
          ;;
             [nN][oO]|[nN])
          exit 1
                ;;
             *)
          echo "Invalid answer..."
          exit 1
          ;;
         esac
        fi

    done
  fi
  install_python_dependencies

  odoo_configuration

  get_ip
  if [ "$HOST" != "$EXTERNAL_IP" ] && [ -z $EMAIL ]; then
    server_configuration
  fi

  if [ "$HOST" != "$EXTERNAL_IP" ] && [ ! -z $EMAIL ];then
    create_ssl_cert
    configur_ssl_server
  fi

  test_the_server
  print_url
}
test_the_server(){
  systemctl start odoo$VERSION-server
  systemctl enable odoo$VERSION-server
  systemctl status odoo$VERSION-server
}
print_url(){
  if [ -z $EMAIL ];then
    HOST=http://$HOST
  else
    HOST=https://$HOST
  fi
  cat 1>&2 <<HERE
         ******************************************************************
         *           Installation completed successfully
         *           URL: $HOST
         ******************************************************************
HERE
}

main "$@" || exit 1
