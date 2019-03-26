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






