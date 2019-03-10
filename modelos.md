# Trucos con los modelos

# Estados
```
RO_STATES = {'draft': [('readonly', False)]}

class HrHourReport(models.Model):
    _name = 'hr.hour.report'
    _description = 'Hoja de Bonos RRHH'
    _inherit = ['mail.thread']
    _order = 'date_issue desc, name desc, id desc'
    
    line_ids = fields.One2many('hr.bonus.line', 'sheet_id', 'Bonos', readonly=True, states=RO_STATES)
```



# Fecha actual
```
date = fields.Date('Fecha contable', default=fields.Date.today)
```

# Cadenas
```
cadena = cadena + u" Socio de Negocio: %s \n"%(socio_negocio)
cadena = notas + '\n' + u" NV: %s \n" % (nv)
```


# Delete
```
alarm_ids = fields.Many2many('calendar.alarm', 'calendar_alarm_calendar_event_rel', string='Reminders', ondelete="restrict", copy=False)
```

# Evita Borrar si tiene valores
```
alarm_ids = fields.Many2many('calendar.alarm', 'calendar_alarm_calendar_event_rel', string='Reminders', ondelete="restrict", copy=False)

CASCADE: Delete the Course record with matching student_id when Student is deleted

RESTRICT: Cannot delete the Student as long as it is related to a Course.

NO ACTION: similar, but is a deferred check: You can delete the Student but you have to make sure that the integrity is OK when the transaction is committed.

SET DEFAULT: uses openerp default definition (see _defaults dict in the python model definition)

SET NULL: when a Student gets deleted, the student_id becomes NULL in the DB.
 
```


# Colocando secuencia a una vista tree
```
sequence = fields.Integer(compute='_compute_sequence')

    @api.multi
    def _compute_sequence(self):
        for i, record in enumerate(self.sorted('id', reverse=True), 1):
            record.sequence = i
```	    
	    
# Parametros
```
limit_day = self.env['ir.config_parameter'].sudo().get_param('cancel.sale.order')
```

# Utilizacion de Mappeed
```
stock = sum(locations.with_context({'template_id': record.id}).mapped('virtual_available'))
```

# Importar Correctamente una Libreria PY
```
try:
	import barcode
	from barcode.writer import ImageWriter
except ImportError as exc:
	_logger.error('Faltan dependencias: %s', exc)
``` 

# Trabajos con Fechas
```
from datetime import datetime, timedelta

@api.one
    @api.depends('desde_date', 'hasta_date')
    def _calcular_si_es_mes(self):
        hoy = datetime.now().date()
        desde = self.desde_date
        fecha_desde = datetime.strptime(str(desde), '%Y-%m-%d')
        if str(fecha_desde) < str(hoy):
            if self.hasta_date:
                hasta_date = datetime.strptime(str(self.hasta_date), '%Y-%m-%d')
                if str(hasta_date) > str(hoy):
                    self.del_mes = True
            else:
                self.del_mes = True
        else:
            self.del_mes = False
```
    
# Campos tipo moneda
```
amount_total = fields.Monetary('Total')
```


# Raise
```
from odoo.exceptions import UserError

raise UserError(_('%s no tiene contrato para el periodo %s - %s') % (employee.display_name, date_from, date_to))

raise UserError(_('El monto por préstamos no coincide:\nCuotas por pagar: %f\nMonto préstamo en nómina: %s') % (round(total_cuotas), round(total_prestamos)))

```	

# Log en campos de estados
```
state = fields.Selection([('pending', 'Pendiente'), ('error', 'Errores')], 'Estado', required=True, track_visibility='onchange')
```

# Crear como admin
```
insert = self.env['tag.list'].sudo().create(vals)
```

# Tratando de Importar una libreria
```
try:
    import pysftp
except ImportError:
    raise ImportError('This module needs pysftp to automaticly write backups to the FTP through SFTP. Please install pysftp on your system. (sudo pip install pysftp)')
 ``` 
 
 # Fecha - Today
```
from datetime import datetime
a = datetime.today()
 ``` 
 
 
 # Redefiniendo Métodos
```
 @api.multi
    def button_mark_done(self):
        if not self.tag_mrp_ids:
            raise ValidationError(_("Importante! Por favor defina los tags"))
        res = super(MrpProduction, self).do_transfer()
        return res
  ``` 
 
 # Parametros
 ```
<?xml version="1.0"?>
<odoo>
    <data noupdate="0">
    	<record id="login_form_disable_footer" model="ir.config_parameter">
            <field name="key">login_form_disable_footer</field>
            <field name="value">False</field>
        </record>
    </data>
</odoo>
 ```  
```
cr = request.cr
uid = odoo.SUPERUSER_ID
param_obj = request.env['ir.config_parameter']

change_background = ast.literal_eval(param_obj.get_param('login_form_change_background_by_hour')) or False
config_login_timezone = param_obj.get_param('login_form_change_background_timezone')
 ```  
 
 
 # Error
```
from odoo.exceptions import ValidationError
raise ValidationError(_("Importante! Por favor defina los tags"))
 ```  
 
 
 
# Herencia en el modelo
```
class SaleOrderNotCopy(models.Model):
    _inherit = "sale.order"
    user_id = fields.Many2one('res.users', copy=False)
 ```  

    
# Obtener datos desde la compañía
```
self.env.user.company_id.name
```

# Stock de un producto
```
stock = sum(id.stock_quant_ids.mapped('qty'))
```


# Tipos de campos en Odoo

```
folio = fields.Integer(string='Folio:', size=10)
name = fields.Char(string='New Value', size=64, required=True)
online_mode = fields.Boolean('Online Mode', help='Si esta activo', default='True')

doc_type = fields.Selection(
            [('D','RUT Chile'),
            ('P','Pasaportes'),
            ('C ','Permiso de conducir Chile '),
            ('I','Carta o documento de identidad'),
            ('X','Permiso de residencia UE'),
            ('N','Permiso de residencia Chile ')],
            'Tipo de Documento', size=1)
            
gender = fields.Selection([('F','Femenino'),('M','Masculino')],'Sexo',size=1)
  
company_id = fields.Many2one('res.company', string='Compañía', change_default=True, readonly=True,
            default=lambda self: self.env['res.company']._company_default_get('traveler.register'))
            
entry_date = fields.Datetime('Fecha de Entrada', default = lambda self: datetime.today()) 


```

# Colocando Valores por defecto

```
@api.model
    def create(self, vals):
        vals['property_payment_term_id'] = 1
        return super(res_partner_cnp, self).create(vals)
  ```      

# Salto de linea
```
'comment': note and note_sale+'\n'+note or note_sale
```

# Cadenas
```
 cadena = u" Dir. Intermediaria: %s, %s \n Dir. Final: %s, %s "%(direccion_1,ciudad,direccion_2,ciudad2)
 ```
 # Redondear con mas decimales
```
 
 monto = fields.Float('Monto', digits=(10, 4))
 ```

# Opciones en los campos básicos en Odoo

```
from openerp import models, fields

class AModel(models.Model):

    _name = 'a_name'

    name = fields.Char(
        string="Name",                   # Optional label of the field
        compute="_compute_name_custom",  # Transform the fields in computed fields
        store=True,                      # If computed it will store the result
        select=True,                     # Force index on field
        readonly=True,                   # Field will be readonly in views
        inverse="_write_name"            # On update trigger
        required=True,                   # Mandatory field
        translate=True,                  # Translation enable
        help='blabla',                   # Help tooltip text
        company_dependent=True,          # Transform columns to ir.property
        search='_search_function'        # Custom search function mainly used with compute
    )
```


# Funcion OnChange
```
    partner_id = fields.Many2one('res.partner','Socio')
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        partner_id = self.partner_id
        if partner_id:
            self.first_name = partner_id.name
            if not partner_id.country_id:
                raise UserError(_('Error 0001: No existe el pais'))
            self.birth_country = partner_id.country_id.id
```


# Calculado comision en la factura
```
total = 0
for line in self.invoice_line_ids:
    if line.product_id:
        total += (line.product_id.sale_commission or 0.0) / 100.0 * line.price_unit * line.quantity
self.sale_commission = total
```


# Clase Inicial Modelo Herencia
```
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime

class LibreDTEResCompany(models.Model):
    _inherit = "res.company"
    libredte_hash = fields.Char('LibreDTE hash', help="Code from LibreDTE")
    dte_preliminar = fields.Boolean('DTE Preliminar', help='Si')
    online_mode = fields.Boolean('Online Mode', help='Si', default='True')
```

# Clase Inicial Modelo Herencia
```
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record model="ir.ui.view" id="webfactura_view_company_inherit_form">
        <field name="name">webfactura.view.company.inherit.form</field>
        <field name="inherit_id" ref="base.view_company_form"/>
        <field name="model">res.company</field>
        <field name="arch" type="xml">
            <notebook>
                <page string="LibreDTE">
                    <group cols="4">
                        <field name="libredte_hash" password="True" class="oe_inline" required="1"/>
                        <field name="dte_preliminar" />
                        <field name="online_mode" />
                    </group>
                </page>
            </notebook>
        </field>
    </record>
</odoo>
```

# Herencia de campo

```
<?xml version="1.0" encoding="UTF-8"?>
 <odoo>
    <data>
        <record model="ir.ui.view" id="partner_instructor_form_view">
            <field name="name">partner.instructor</field>
            <field name="model">res.partner</field>
            <field name="inherit_id" ref="base.view_partner_form"/>
            <field name="arch" type="xml"> 
               <field name="category_id" position="after" >          
                    <field name="rut" string="RUC:" placeholder="00000000" />
                    <field name="mail" string="Correo"/> 
               </field>                       
            </field>
        </record>
    </data>
</odoo>

```

# Clase Inicial Modelo
```
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class rrhh_afp(models.Model):
    _description = "AFP Fondo de Pension"
    _name = 'rrhh.afp'

    codigo = fields.Char('Codigo', required=True)
    name = fields.Char('Name', translate=True)
    rut = fields.Char('Rut', translate=True)
    tasa = fields.Float('Tasa', required=True)
    sis = fields.Float('Aporte Empresa', required=True)
    independiente = fields.Float('Independientes', required=True)
```

# Clase Inicial Vista
```
<?xml version="1.0" encoding="UTF-8"?>
 <odoo>
    <data>

    <record id="view_form_rrhh_afp" model="ir.ui.view">
             <field name="name">view.form.rrhh.afp</field>
             <field name="model">rrhh.afp</field>
             <field name="arch" type="xml">
                <form string="Listado de AFP">
                  <sheet>
                    <legend>AFP</legend>
                       <group>
                          <group>
                             <field name="rut"/>
                             <field name="name"/>
                             <field name="codigo"/>
                             <field name="tasa"/>
                             <field name="sis"/>
                             <field name="independiente"/>
                          </group>
                       </group>
                   </sheet>
                </form>
            </field>
    </record>

    <record id="view_tree_rrhh_afp" model="ir.ui.view">
             <field name="name">view.tree.rrhh.afp</field>
             <field name="model">rrhh.afp</field>
             <field name="arch" type="xml">
                <tree>
                             <field name="rut"/>
                             <field name="name"/>
                             <field name="codigo"/>
                </tree>
            </field>
    </record>

    <record id="action_rrhh_afp" model="ir.actions.act_window">
            <field name="name">AFP</field>
            <field name="res_model">rrhh.afp</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
              <p class="oe_view_nocontent_create">
                Presione para crear nuevo Registro</p>
           </field>
    </record>

    <menuitem id="rrhh_afp_menu"
        name="AFP"
        parent="menu_payroll_config"
        sequence="31"
        action="action_rrhh_afp" />

     </data>
</odoo>
```

# Cargar Datos
```
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data noupdate="1">
        <record id="rrhh_afp_01" model="rrhh.afp">
            <field name="name">Capital</field>
            <field name="rut">00000000-0</field>
            <field name="codigo">34</field>
            <field name="tasa">11.44</field>
            <field name="sis">1.41</field>
            <field name="independiente">12.85</field>
        </record>
        <record id="rrhh_afp_02" model="rrhh.afp">
            <field name="name">Cuprum</field>
            <field name="rut">00000000-0</field>
            <field name="codigo">03</field>
            <field name="tasa">11.48</field>
            <field name="sis">1.41</field>
            <field name="independiente">12.89</field>
        </record>
    </data>
</odoo>
```
# Ejemplo de manifest
```
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2017 Marlon Falcón Hernandez
#    (<http://www.falconsolutions.cl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Base Chilean location MFH',
    'version': '10.0.0.1.0',
    'author': "Falcón Solutions, Luis Torres...",
    'maintainer': 'Falcon Solutions',
    'website': 'http://www.falconsolutions.cl',
    'license': 'AGPL-3',
    'category': 'Localization/Chile',
    'summary': 'Chilean location: Load basic data.',
    'depends': [
                'base',
                'base_vat',
                'product',
                'account_accountant',
                ],
    'external_dependencies': {
                'python': [
                            'M2Crypto',
                            'elaphe',
                            'cchardet',
                            'rsa'
                            ],
     },
    'description': """
Módulo basado en localización Chilena
=====================================================
1-. Add SII Economical Activities.\n
2.- Load data Counties.\n
3.- Load default value in the country field in view of company and partners.\n
4.- Add Ubication field in view of company and partners.\n
5.- Incorporate a field with the RUT (VAT) formatted according chilean customs.\n
6.- This module validates the RUT directly.\n
""",
    'data': [
            'views/base_view.xml',
            'views/economical_activities.xml',
            'report/report_invoice.xml',
            'data/email_template.xml',
            'views/res_partner.xml',
            'data/uom_data.xml',
            ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,

}
```

# Campo Many2one
```
functional_area_id = fields.Many2one('functional.area', 'Areas Funcionales')
```

# Ocultar campo en la vista que depende de otro
```
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record model="ir.ui.view" id="stock_picking_inherit_form">
        <field name="name">stock.picking.inherit.form</field>
        <field name="inherit_id" ref="stock.view_picking_form"/>
        <field name="model">stock.picking</field>
        <field name="arch" type="xml">
            <field name="partner_id" position="after" >
                    <field name="electronic_picking" />
                      <field name="patente" placeholder="AA0000" attrs="{'invisible': ['|',('electronic_picking', '=', False)]}"/>
            </field>
        </field>
    </record>
</odoo>
```

# Conocer el ID
```
var = self.env['res.country'].search([('name','=','Chile')])
        self.fax = var.id
```

# Campos relacionados
```
online_mode_f = fields.Boolean('Online', related='company_id.online_mode')
```

```
 <field name="team_id" position="after" >
    <field name="online_mode_f" invisible="1" />
    <field name="number_folio" attrs="{'invisible':[('online_mode_f','=', True)]}"/>
</field>
```

# Log odoo
```
import logging
```

```
_logger.info('Not be found data to update the currency %s!',currency.name)
```


# Exportación TXT
```
@api.multi
    def download_txt(self):
        res = {}
        op = self.operation == 'sale' and 'VENTAS' or 'COMPRAS'
        fname = '%s_%s_%s_Comprobantes.txt' %(self.company_id.cuit,self.period.replace('-','_'),op)
        path = '/tmp/' + fname
        txtFile = open(path, 'wb')
        for invoice in self.invoice_ids:
            line = ''
            partner = invoice.partner_id.parent_id and invoice.partner_id.parent_id or invoice.partner_id
            line+= invoice.date_invoice.replace("-", '') #fecha factura
            txtFile.write(self.clean_accents(line)+'\n')
        txtFile.close()
        data = base64.encodestring(open(path, 'r').read())
        attach_vals = {'name': fname, 'datas': data, 'datas_fname': fname}
        doc_id = self.env['ir.attachment'].create(attach_vals)
        res['type'] = 'ir.actions.act_url'
        res['target'] = 'new'
        res['url'] = "web/content/?model=ir.attachment&id=" + str(
            doc_id.id) + "&filename_field=datas_fname&field=datas&download=true&filename=" + str(doc_id.name)
        return res
`

```
# Campo autocalculados
```
    estimado = fields.Float('Estimado')
    pagado = fields.Float('Pagado')
    restante = fields.Float(compute='calcular_restante')

    @api.one
    @api.depends('estimado','pagado')
    def calcular_restante(self):
        self.restante = self.estimado - self.pagado
 ```
 
 
 
# Crear una Secuencia
En el modelo
```
name = fields.Char('Código', translate=True, default="Nuevo")
@api.model
    def create(self, vals):
        if vals.get('name', "Nuevo") == "Nuevo":
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.haberesydesc') or "Nuevo"
        return super(hr_haberesydesc, self).create(vals)
```
En data
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="seq_hr_haberesydesc" model="ir.sequence">
            <field name="name">Haberes y Descuentos</field>
            <field name="code">hr.haberesydesc</field>
            <field name="prefix">HD</field>
            <field name="padding">5</field>
            <field name="company_id" eval="False"/>
        </record>
    </data>
</odoo>
```

# Crear valores por defecto en Campos

```
pass_cert = fields.Char('Llave Privada', help="Ruta absoluta del archivo que contiene la llave privada (.key)",
                                default="/opt/odoo/certificados/ghf.key")
```



# Validar campos antes de guardar la factura


```

from odoo.exceptions import ValidationError


    @api.constrains('name')
    def _check_codigo_point_sales(self):
        if len(self.name) < 4:
            raise ValidationError("El Punto de Venta tiene que tener 4 dígitos")
```

# Recorrer un campo many2one
```
    @api.onchange('rh_cargas_ids')
    def onchange_cargas(self):
        c_familiar = 0
        for cargas in self.rh_cargas_ids:
            if cargas.list_tipo == '1':
                c_familiar = c_familiar + 1
        self.cant_carga_familiar = c_familiar
```

# Validar antes de guardar
```

@api.constrains('name')
    def _check_codigo_point_sales(self):
        if len(self.name) < 4:
            raise ValidationError("El Punto de Venta tiene que tener 4 dígitos")
            
```

# LLamar a un metodo de otro modelo 
```
 self.env['modelo.llamar']._metodomodelo()
            
```
# LLamar a un metodo si cargamos una vista
```
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        self.env['maintenance.work.order']._check_work_order_id()
        print "Hello"
        return super(maintenance_tree, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                        submenu=submenu)
            
```

# LLamar a compañia          
```
company_id = fields.Many2one('res.company', string="Company", required=True,
                                 default=lambda self: self.env.user.company_id.id)
                                             
```
# LLamar a logo en qweb        
```

<img t-if="o.company_id.logo" t-att-src="'data:image/png;base64,%s' % o.company_id.logo"
                                style="max-height:170px; width:auto; margin:10px;"/>
                                
```
                                
# Cambiar Nombre
```
@api.multi
    def name_get(self):
        res = super(res_partner, self).name_get()
        result = []
        for element in res:
            partner_id = element[0]
            rut = self.browse(partner_id).document_number
            name = rut and '[%s] %s'%(rut,element[1]) or '%s'%element[1]
            result.append((partner_id,name))
        return result
```

# Recorrer Modelos Ejemplo Facturas
```
        invoice_obj_out_invoice = self.env['account.invoice'].search([('type','=','out_invoice')])
        for id in invoice_obj_out_invoice:
            iva_debito_fiscal = iva_debito_fiscal + id.amount_tax
 ```
 
 
 # Uso de periodos de fechas y recorrerlos
 ```
 
        invoice_obj = self.env['account.invoice']

        date = datetime.strptime(self.date, '%Y-%m-%d')
        end_of_month = monthrange(date.year, date.month)[1]
        start_period = '%s-%s-01' % (date.year, date.month)
        end_period = '%s-%s-%s' % (date.year, date.month, end_of_month)

        invoice_obj_out_invoice= invoice_obj.search([
            ('state', 'in', ['open', 'paid']),
            ('type', '=', 'out_invoice'),
            ('date_invoice', '>=', start_period),
            ('date_invoice', '<=', end_period)
        ])

        invoice_obj_in_invoice = invoice_obj.search([
            ('state', 'in', ['open', 'paid']),
            ('type', '=', 'in_invoice'),
            ('date_invoice', '>=', start_period),
            ('date_invoice', '<=', end_period)
        ])


        # Facturas de Ventas
        # invoice_obj_out_invoice = self.env['account.invoice'].search([('type','=','out_invoice')])
        for id in invoice_obj_out_invoice:
            iva_debito_fiscal = iva_debito_fiscal + id.amount_tax
 ```
  
        
# Crear log
 ``` 
self.message_post(body=_("Se ha enviado un mensaje a " + cto + ": " + ctext))

```

# BD
 ``` 

[databases]
* = host=jamoXXX.cr2z2c7klykx.eu-west-1.rds.amazonaws.com port=5432 user=dbadmin password=XXXXX

[pgbouncer]
;logfile = /var/log/postgresql/pgbouncer.log
pidfile = /var/run/postgresql/pgbouncer.pid
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = trust
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
server_reset_query = DISCARD ALL
server_check_query = select 1
server_check_delay = 10
max_client_conn = 10000
default_pool_size = 20
log_connections = 1
log_disconnections = 1
ignore_startup_parameters = extra_float_digits
server_idle_timeout = 240
admin_users = dbadmin
stats_users = dbadmin
 ```                                    
                                
  
