python /opt/odoo/server/odoo-bin shell -c /etc/odoo/odoo.conf -d db10-chile-sii

env['hr.employee'].search([])

env['ir.ui.view'].browse(1255).write({'active': False})

env.cr.commit()

ipython
