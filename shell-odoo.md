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

# Borrar mensajes
```
su - odoo -s /bin/bash
python /opt/odoo/server/odoo-bin shell -c /etc/odoo/odoo.conf -d db10-chile-sii
message=env['mail.message'].search([('date','<','2022-01-01')])
message.unlink()
env.cr.commit()

message=env['mail.message'].search([('date','<','2019-08-01'),('model','<>','chile.audit')], limit=100)
```

# Paso1 Eliminar cuentas de clientes
```
odoo-bin shell -d ofinubeas-hergo-hergo002-667745
partners=env['res.partner'].search([])
partners.write({'property_account_receivable_id': False, 'property_account_payable_id': False})
env.cr.commit()

#CC
env['account.account'].search([]).unlink()

for account in env['account.account'].search([]):
    try:
        account.unlink()
    except:
        pass

```
Actualizar
```
odoo-bin -d db10-chile-sii -d
```
```
for account in accounts:
    try:
        account.unlink()
        print('borrado')
    except:
        print('no pudo borrar')```
