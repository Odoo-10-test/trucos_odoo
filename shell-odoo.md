# Consultas rápidas a Odoo
```
su - odoo -s /bin/bash
luego ejecutas este comando para entrar en modo "shell":
python /opt/odoo/server/odoo-bin shell -c /etc/odoo/odoo.conf -d db10-chile-sii
y luego ejecutas ahí mismo este comando:
env['sii.invoice'].search([]).unlink()
Para que los cambios se apliquen, ahí mismo en modo shell escribes:
env.cr.commit()
Y listo, ya podrás salir con CTRL+D
```
