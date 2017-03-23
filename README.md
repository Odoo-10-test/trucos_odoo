# trucos_view

# Remplazar de posicion un campo

Quito el campo de la vista

´´´
<field name="campo" position="replace"/>
´´´

Lo agrego en otra posición
´´´
<field name="otro_campo" position="after">
<field name="campo"/>
</field>
´´´

# Hacer un campo solo lectura
´´´
<field name="street" position="replace">
    <field name="street" required="1"/>
</field>
´´´






