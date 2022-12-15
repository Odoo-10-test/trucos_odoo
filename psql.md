# Conectarnos en MAC
```
psql postgres
\l
\c db14-spain
```

# Tamaño de la BD
```
sudo -u postgres psql
\l
SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS SIZE FROM pg_database;
```

# Paramos los cron
```
sudo -u postgres psql -d credit
UPDATE ir_cron SET active=false;
SELECT * FROM ir_cron;
```

# Borrar BD
```
sudo -u postgres psql
\l
DROP DATABASE "db10";
```

# Listar BD
```
sudo -u postgres psql -c "\l+"
```

# Listar las BD
```
\l
```

# Terminar 
```
\q
```

# Listar Tablas
```
\dt
```

# Listar Registro de una tabla
```
SELECT * FROM res_users;
\dt
```

# Cambiar pass de admin
```
sudo -u postgres psql -d db10-chile-sii
UPDATE res_users SET password='x1234567890', password_crypt='HASH' WHERE login='admin';
```

# Cambiar pass de admin 14
```
sudo -u postgres psql -d db10-chile-sii
update res_users set password='123' where login='admin';
```
# Borrar Facturas en Borrador
```
sudo su - postgres
psql
\c db10-chile-sii
DELETE FROM account_invoice WHERE state = 'cancel';
```

# Borrar Pagos en Draft
```
sudo su - postgres
psql
\c db10-chile-sii
DELETE FROM account_payment WHERE state = 'draft';
```
# Borrar Cola
```
sudo su - postgres
psql
\c db10-chile-sii
DELETE FROM sii_process_queue;
```





