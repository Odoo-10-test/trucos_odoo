python3 /opt/odoo/server/odoo-bin shell -c /etc/odoo/odoo.conf -d db12-chile-sii
products=env['product.template'].search([('type', '=', 'consu')])
for product in products:
    try:
        print(product.id)
        print('Modificando')
        product.type = 'product'
    except:
        print('error')

env.cr.commit()
