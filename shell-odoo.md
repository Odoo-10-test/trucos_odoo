# Consultas rápidas a Odoo
```
python /opt/odoo/server/odoo-bin shell -c /etc/odoo/odoo.conf -d db10-chile-sii
env['hr.employee'].search([])
env['ir.ui.view'].browse(1255).write({'active': False})
env.cr.commit()
ipython

su - odoo -s /bin/bash
luego ejecutas este comando para entrar en modo "shell":
python /opt/odoo/server/odoo-bin shell -c /etc/odoo/odoo.conf -d db10-chile-sii
y luego ejecutas ahí mismo este comando:
env['sii.invoice'].search([]).unlink()
Para que los cambios se apliquen, ahí mismo en modo shell escribes:
env.cr.commit()
Y listo, ya podrás salir con CTRL+D
```
