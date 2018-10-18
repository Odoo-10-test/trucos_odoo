# Borrar BD
```
sudo su postgres
dropdb db10-chile-sii


psql
dropdb 'db10-chile-sii'
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


