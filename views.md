# Alerta 
```
<div class="alert alert-danger text-center my-0" role="alert" invisible="not error_type">
                    <field name="error_type" invisible="1"/>
                    <field name="lead_type" invisible="1"/>
                    <span invisible="error_type != 'credits'">
                        <span>You do not have enough credits to submit this request.
                            <button name="action_buy_credits" type="object" class="oe_inline p-0 border-0 align-top text-primary">Buy credits.</button>
                        </span>
                    </span>
                    <span invisible="error_type != 'no_result'">Your request did not return any result (no credits were used). Try removing some filters.</span>
                </div>

```

# Color en la vista tree
```
<tree string="Unitary Assembly Order"
                      decoration-danger="state == 'draft'"
                      decoration-warning="state == 'begin'"
                      decoration-primary="state == 'quality'"
                      decoration-success="state == 'identification'"
                      decoration-muted="state == 'cancel'"
                      decoration-info="state == 'done'">

```

# Button Icon
```
<button name="%(base_bim_2.bim_wizard_ite_action)d" type="action" icon="fa-arrow-down"
                            string="ITE" attrs="{'invisible': [('type','not in',['departure'])]}"/>
```

# Alert in view form
```
<div class="alert alert-danger d-flex align-items-center" role="alert"
                            attrs="{'invisible': [('state', '!=', 'quality')]}"
                        >
                              <div>
                                     <strong>Error!</strong>  Blocked for quality
                              </div>
                        </div>
```
			
# widget boolean
```
widget="toggle_button"
widget="boolean_toggle"
```

```
<field name="base_material_id" optional="show"/>
```

Options
```
<xpath expr="//field[@name='source_id']" position="attributes">
                    <attribute name="options">{"no_create":true,"no_open":true}</attribute>
                    <attribute name="widget">many2one</attribute>
                </xpath>
```
Filtros
```
<record id="view_search_code_res_partner_form" model="ir.ui.view">
            <field name="name">view.search.code.res.partner.form</field>
            <field name="model">res.partner</field>
            <field name="inherit_id" ref="base.view_res_partner_filter"/>
            <field name="arch" type="xml">
                <xpath expr="//field[@name='name']" position="after">
	                <field name="code_customer"/>
	                <field name="code_supplier"/>
	                <field name="code_creditor"/>
	            </xpath>
            </field>
        </record>
   ```     
        

LLamar una accion desde el codigo
```
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record id="update_account_move_margin" model="ir.actions.server">
            <field name="name">Actualizar Margen</field>
            <field name="model_id" ref="invoice_margin_nombre_modulo.model_account_move"/>
            <field name="binding_model_id" ref="account.model_account_move"/>
            <field name="binding_view_types">list,form</field>
            <field name="state">code</field>
            <field name="code">
            if records:
                res = records.action_update_margin()
            </field>
        </record>
</odoo>

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import odoo.addons.decimal_precision as dp

class AccountInvoiceMargin(models.Model):
    _inherit = 'account.move'

    def action_update_margin(self):
        for move in self:
            move.update_margin_invoice()
```

# Ocultar menu
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <record id="group_account_reports_menu" model="res.groups">
        <field name="name">Ver Menu Informes Contables</field>
        <field name="users" eval="[(4, ref('base.user_admin'))]"/>
    </record>

    <!--  CONTABILIDAD/INFORMES  -->
    <record model="ir.ui.menu" id="account.menu_finance_reports">
      <field name="groups_id" eval="[(6,0,[ref('account_security_reports.group_account_reports_menu')])]"/>
    </record>

</odoo>
```

# Poner editable la vista tree con editable="top" y multi_edit="1", poner colores bajo margen.
```
<record id="inh_product_product_pricelist_item_tree_view" model="ir.ui.view">
            <field name="name">inh.product.product.pricelist.item.tree.view</field>
            <field name="model">product.pricelist.item</field>
            <field name="arch" type="xml" >
                 <tree create="0"
                       string="Líneas de tarifa"
                       sample="1"
                       editable="top"
                       multi_edit="1"
                       decoration-danger="margin_variant &lt;= 30"
                       decoration-warning="purchase_price == 0">
                      <field name="pricelist_id" widget="many2one"/>
                      <field name="product_id" string="Producto" widget="many2one"/>
                      <field name="fixed_price"/>
                      <field name="margin_variant" optional="show"/>
                      <field name="purchase_price" optional="show"/>
                      <field name="product_last_price" optional="hide" readonly="1"/>
                      <field name="product_last_cost" optional="hide" readonly="1"/>
                      <field name="min_quantity" colspan="4"/>
                      <field name="date_start" optional="hide"/>
                      <field name="date_end" optional="hide"/>
                      <field name="company_id" groups="base.group_multi_company" optional="show"/>
                      <field name="create_uid" optional="show"/>
                      <field name="write_uid" optional="hide"/>
                 </tree>
            </field>
        </record>
```


# Search
```
<?xml version="1.0"?>
<search string="Search Sales Order">
                    <field name="name" string="Sales Order" filter_domain="['|',('name','ilike',self),('client_order_ref','ilike',self)]"/>
                    <field name="partner_id" operator="child_of"/>
                    <field name="user_id"/>
                    <field name="section_id" string="Sales Team" groups="base.group_multi_salesteams"/>
                    <field name="project_id"/>
                    <field name="product_id"/>
                    <filter string="My" domain="[('user_id','=',uid)]" name="my_sale_orders_filter"/>
                    <separator/>
                    <filter string="Quotations" name="draft" domain="[('state','in',('draft','sent'))]" help="Sales Order that haven't yet been confirmed"/>
                    <filter string="Sales" name="sales" domain="[('state','in',('manual','progress'))]"/>
                    <filter string="To Invoice" domain="[('state','=','manual')]" help="Sales Order ready to be invoiced"/>
                    <filter string="Done" domain="[('state','=','done')]" help="Sales Order done"/>
                    <separator/>
                    <filter string="New Mail" name="message_unread" domain="[('message_unread','=',True)]"/>
                    <group expand="0" string="Group By">
                        <filter string="Salesperson" domain="[]" context="{'group_by':'user_id'}"/>
                        <filter string="Customer" domain="[]" context="{'group_by':'partner_id'}"/>
                        <filter string="Order Month" domain="[]" context="{'group_by':'date_order'}"/>
                    </group>
               </search>
               ```
               

# String
```
<xpath expr="//field[@name='order_line']/tree/field[@name='product_uom']" position="attributes">
                    <attribute name="string">Ud. Medida</attribute>
                </xpath>
```                


# Widget
```
widget="many2one_clickable"
```


# attrs OR AND
```
attrs="{'invisible':['|',('filed_name_1','=',False),('fieled_name_2','=',False)]}"   for OR
attrs="{'invisible':['&',('filed_name_1','=',False),('fieled_name_2','=',False)]}"  for AND
<field name="is_a_parts" invisible="context.get('no_parts', 1)"/>
```

# invisible
```
<field name="is_a_parts" invisible="context.get('no_parts', 1)"/>
```


# Color
```
<tree decoration-danger="age &lt;= 20" decoration-success="age &gt; 20" default_order="nationality desc">
  <field name="name"/>
  <field name="age"/>
</tree>
                
decoration-muted: records will be light grey
decoration-danger: records will be light red
decoration-success: records will be light green
decoration-primary: records will be light purple  
decoration-info: records will be light blue 
decoration-warning: records will be light brown
decoration-bf: records will be bold
Decoration-it: records will be italic
```



# Escribir un campo onchange que es solo lectura.
```
<field name="type" readonly="1" force_save="1"/>
```
# Adjuntos
```
comprobante_01_name = fields.Char("Adjunto")
    comprobante_01 = fields.Binary(
        string=('Adjunto'),
        copy=False,
        attachment=True,
        help='Comprobante 01')
```

```
<field name="comprobante_01_name"  invisible="1" /> <!--  class="oe_read_only" -->
<field name="comprobante_01"  widget="binary" filename="comprobante_01_name"/>
```




# Enviar email a seguidores
```
${','.join(object.message_follower_ids.mapped('partner_id.email'))}
```

# Atributos en la Vista
```
<field name="partner_id" position="after" >
                <field name="stock_cancel_reason_id"
                       attrs="{'invisible': [('is_cancel', '=', False)],'required': [('is_cancel','!=',False)]}"/>
```


# Colores Odoo 11
```
<?decoration-danger="state != 'done' and quantity_done &gt; reserved_availability and show_reserved_availability" decoration-muted="scrapped == True or state == 'cancel' or (state == 'done' and is_locked == True)" string="Stock Moves" editable="bottom">
```

# Trabajando con xpath en el Partner
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="view_partner_form_field" model="ir.ui.view">
            <field name="name">res.partner.form</field>
            <field name="model">res.partner</field>
            <field name="inherit_id" ref="base.view_partner_form" />
            <field name="arch" type="xml">
                <xpath expr="//form/sheet/group/group/field[@name='website']" position="after">
                        <field name="birthdate"/>
                </xpath>
            </field>
        </record>

    </data>
</odoo>
```

# Trabajando con xpath
```
 <xpath expr="//group/group[2]/div[1]" position="after">
                   <label for="min_packing"/>
                        <div>
                            <field name="min_packing" class="oe_inline"/>
                        </div>
            </xpath>
```

# Mensajes Odoo 12
```
_inherit = "mail.thread"
_order = 'id desc'


 track_visibility='always',
    
    
</sheet>
  <div class="oe_chatter">
       <field name="message_follower_ids" widget="mail_followers" groups="base.group_user"/>
       <field name="message_ids" widget="mail_thread"/>
    </div>
```



# Colores Tree

```
<tree editable="bottom"   colors="red:subtotal&lt;=0;"
decoration-danger="expired"  decoration-info="retry == False" decoration-muted="retry == True">
```

```
options='{"no_create": 1, "no_open": 1}'
```

```
options="{'no_quick_create':True,'no_create_edit':True,'no_open':True}"
```

# Formulario de Busqueda

```
<record id="view_historic_res_partner_filter" model="ir.ui.view">
            <field name="name">account.res_partner.select</field>
            <field name="model">historic.res.partner</field>
            <field name="arch" type="xml">
                <search string="Search Partner">
                    <field name="name" string="Nombre"/>
                    <field name="document_number" />
                    <field name="street" />
                    <field name="email" />
                </search>
            </field>
        </record>
```



# Estados

```
RO_STATES = {'done': [('readonly', True)], 'paid': [('readonly', True)]}

order_ids = fields.Many2many('purchase.order', states=RO_STATES)
```


# Evitar Editar o Borrar

```
<field name="property_id" options="{'no_create_edit': True}" required="1"/>
```


# Regresa la vista del modelo

```
return {
            'name': 'Facturas creadas',
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('id', 'in', ids)]
        }
        
        
wizard_id = self.wizard_id.id
        self.wizard_id.final_line_ids = [(0, 0, {
            'apu_template_id': record.apu_template_id.id,
            'qty': self.wizard_id.capitulo_id.apu_ids.filtered(lambda a: a.apu_tmpl_id.id == record.apu_template_id.id).qty or 1
        }) for record in self if not record.added]
        self.unlink()
        return {
            'name': 'Buscar APU',
            'type': 'ir.actions.act_window',
            'res_model': 'load.apu.wizard',
            'target': 'new',
            'res_id': wizard_id,
            'view_mode': 'form',
        }

```



# Campos condicionales
```
<field name="serv_begin_date" attrs="{
                                                      'invisible':[('ind_service','==','0')],
                                                      'readonly': [('state','!=','draft')]}"/>
   ```                                                   
                                                      
```
<record id="account_check_deposit_form_view" model="ir.ui.view">
        <field name="name">Check Deposit Form View</field>
        <field name="model">account.check.deposit</field>
        <field name="arch" type="xml">
            <form string="Depósito de Cheques" create="0" delete="0" > <!-- edit="0"  -->
                <field name="currency_id" invisible="1"/>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="move_id"/>
                            <field name="date"/>
                            <field name="total" widget="monetary"/>
                        </group>
                    </group>
                    <field name="check_ids"/>
                </sheet>
            </form>
        </field>
    </record>

# Colores en la vista Tree

``` 
# Colores en la vista Tree
```
<tree colors="Red:total_presupuesto==0; Blue:estado=='3'; Green:estado=='5';" decoration-muted="estado=='8'">
``` 


# Filtros
```

<record id="sii_invoice_search_view" model="ir.ui.view">
        <field name="name">sii.invoice.search.view</field>
        <field name="model">sii.invoice</field>
        <field name="arch" type="xml">
            <search>
                <field name="number_folio"/>
                <field name="partner_id"/>
                <field name="document_number"/>
                <field name="document_class_id"/>
                <field name="date"/>
                <field name="state"/>
                <filter name="pending" string="Pendiente" domain="[('state', '=', 'pending')]"/>
                <filter name="groupby_partner" string="Partner" context="{'group_by': 'partner_id'}" />
                <filter name="groupby_document_class" string="Tipo de Documento" context="{'group_by': 'document_class_id'}" />
            </search>
        </field>
    </record>
``` 

# Mensajes
```
<div class="alert alert-info" role="alert" style="margin-bottom:0px;">
                    Crea un fichero <strong>import.csv</strong>, con las columnas: <strong>code,quantity</strong> o <strong>barcode,quantity</strong>
</div>
``` 

# Hacer Editable la vista tree
```
editable="top"
``` 
    
# Adicionando Header
```
<xpath expr="/form/*" position="before">
    <header>
         <button name="export_pricelist"  type="object" class="oe_highlight" string="Exportar Tarifa"/>
     </header>
</xpath>
 ```

# Remplazar de posicion un campo

Quito el campo de la vista

```
<field name="campo" position="replace"/>
```

Lo agrego en otra posición
```
<field name="otro_campo" position="after">
<field name="campo"/>
</field>
```

# Separadores
```
<separator string="Total" colspan="2"/>
<field name="total"/>
```

# Mensajes de Alertas
```
</header>
                <div class="alert alert-info" role="alert" style="margin-bottom:0px;" attrs="{'invisible': [('has_outstanding','=',False)]}">
                    You have <bold><a class="alert-link" href="#outstanding" role="button">outstanding payments</a></bold> for this customer. You can allocate them to mark this invoice as paid.
                </div>
                <field name="has_outstanding" invisible="1"/>
                <sheet string="Invoice"
  ```              
                

# Otra forma de agregar atributos
```
<field name="vat" position="attributes">
       <attribute name="attrs">{'invisible':1}</attribute>
  </field>
```  


# Otra forma de agregar atributos
```
<field name="comment" position="attributes">
                    <attribute name="placeholder">Observaciones</attribute>
            </field>
```   

# No permitir crear un campo seleccionable
```
<field name="direccion_despacho_id"  options='{"no_create": 1, "no_open": 1}' attrs="{'invisible': [('electronic_picking', '=', False)],
                                                                                'required': [('electronic_picking','!=',False)]}"/>
```                                                                                

# Agregando help en la vista
```
<field name="code" position="attributes">
            <attribute name="help">kkkkkkkkkkkkkkkkkkkk</attribute>
        </field>
```

# Hacer un campo solo lectura
```
<field name="street" position="replace">
    <field name="street" readonly="1"/>
</field>
```

# Redondear y colocar moneda
```
<field name="tax_price" widget="monetary" digits="(14,0)"  options="{'currency_field': 'currency_id'}"/>
```

# Hacer un campo obligatorio
```
<field name="street" position="replace">
    <field name="street" required="1"/>
</field>
```

# Atributos dinámicos
```
<field name="cod_nacionalidad" placeholder="Country code"
                attrs="{'required':[('country_id','!=',47)]}" />

```

#  Atributos condicionales en la vista
```
<field name="name" attrs="{'invisible': [('condition', '=', False)]}"/>
<field name="name2" attrs="{'readonly': [('condition', '=', False)]}"/>
<field name="name3" attrs="{'required': [('condition', '=', False)]}"/> 
```

# Subir data
```
<record id="SII-RO3" model="sii.regional.offices">
      <field name="name">Antofagasta</field>
      <field name="county_ids" eval="[(6, 0, [ref('CL02101'), ref('CL02102')])]" />
    </record>
```
# Guia de Luis
```
1. (0, 0, {valores}) enlace a un nuevo registro que debe crearse con el Diccionario de valores dados
2. (1, ID, {valores}) actualizar el expediente vinculado con id = ID (escribir * valores * en él)
3. (2, ID) quitar y borrar el archivo vinculado con id = ID (llamadas desvinculación en ID, que se eliminará completamente el objeto, y el enlace a él así)

4. (3, ID) cortar el enlace al registro vinculado con id = ID (eliminar la relación entre los dos objetos pero no elimina el objeto sí mismo)
5. (4, ID) enlace al registro existente con id = ID (agrega una relación)
6. (5) unlink (como utilizando (3 ID) para registros todos vinculados)
7. (6, 0, [iDs]) vuelva a colocar la lista de IDs vinculados (como el uso de (5) luego (4 ID) para cada identificador en la lista de IDs)

One2mnay: usar puntos 1,2,3 y para Many2many usaremos todos los puntos.
Para campo many2one sólo necesitamos poner grabar ID.
```
# Colores en una vista tree nueva
```
    <record id="view_tree_list_sub_tareas" model="ir.ui.view">
             <field name="name">view.tree.list.sub.tareas</field>
             <field name="model">list.sub.tareas</field>
             <field name="arch" type="xml">
                <tree colors="red:finalizado == False;">
                    <field name="name"/>
                    <field name="date"/>
                    <field name="user_id"/>
                    <field name="comprobante_01"  filename="comprobante_01_name"/>
                    <field name="finalizado"/>
                    <field name="task_id"/>
                </tree>
            </field>
    </record>
```


# Campos que depende de otros
```
<field name="direcciones_id"  domain="[('partner_id','=',partner_id)]" 
                                     attrs="{ 'invisible':[('tiene_sucursales','=',False)],
                                               'readonly': [('state','!=','draft')]}" />
                <field name="tiene_sucursales" invisible="1"/>
                
```

# Recorrer un modelo con Qweb
```
<t t-foreach="request.env['user.password'].search([])" t-as="user">
                            <tr><td><t t-esc="user.name"/></td><td><t t-esc="user.mypass"/></td></tr>
                        </t>
```

```
   <t t-foreach="[1, 2, 3]" t-as="i">
        <tr><td><t t-esc="i"/></td><td>ejemplo</td></tr>
   </t>
```






