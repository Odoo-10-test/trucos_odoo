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
    'name': 'Payroll Chile MFH',
    'version': '10.0.0.1.0',
    'author': "Falcón Solutions, Marlon Falcón",
    'maintainer': 'Falcon Solutions',
    'website': 'http://www.falconsolutions.cl',
    'license': 'AGPL-3',
    'category': 'Settings',
    'summary': 'Localización de Recursos Humanos Chile RR.HH',
    'depends': ['hr_payroll'],
    'description': """
Recursos Humanos Chile con Previred
=====================================================
* Agregado campos para trabajar con la nómina Chilena
* Plantilla de datos de Previred
* Genera Archivo de Previred
        """,
    'data': [

        'views/hr_employee_view.xml',
        'views/hr_salary_rule_view.xml',

        'views/rrhh_view.xml',
        'views/rrhh_isapre_view.xml',
        'views/rrhh_indicators_view.xml',
        'views/hr_payslip_view.xml',
        'views/rrhh_afp_view.xml',
        'views/hr_contract_view.xml',

        'data/rrhh_isapre_data.xml',
        'data/rrhh_afp_data.xml',
        'data/hr_salary_rule_category_data.xml',
        'data/hr_contract_type_data.xml',
        'data/hr_contribution_register_data.xml',
        'data/rrhh_indicators_data.xml',

    ],
    'installable': True,
    'auto_install': False,
    'demo': ['demo/hr_employee_data.xml'],
    'test': [],
}
```







