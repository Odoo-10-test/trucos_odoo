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

# Otra forma de agregar atributos
```
<field name="vat" position="attributes">
       <attribute name="attrs">{'invisible':1}</attribute>
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







