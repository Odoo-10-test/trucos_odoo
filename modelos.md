# Trucos con los modelos

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
            
                                
                                
  
