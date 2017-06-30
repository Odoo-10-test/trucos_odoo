# trucos_view

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






