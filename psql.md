# Listar las BD
```
\l
```

# Terminar 
```
\q
```

# Cambiar pass de admin
```
sudo -u postgres psql -d db10-chile-sii
UPDATE res_users SET password='x1234567890', password_crypt='HASH' WHERE login='admin';
```
