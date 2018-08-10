# Trucos de Reportes

# If
```
<span t-if="o.direcciones_id.street2">
  <strong>Dirección&#160;&#160;&#160;&#160;:</strong> <span t-field="o.direcciones_id.street" /> , 
  <span t-field="o.direcciones_id.street2" /><br/>
</span>

<span t-if="not o.direcciones_id.street2">
   <strong>Dirección&#160;&#160;&#160;&#160;:</strong> <span t-field="o.direcciones_id.street" /><br/>
</span>
```

# Suma de Elementos
```
<t t-set="test_variable" t-value="100"/>
<p t-foreach="[10, 20, 30]" t-as="i"> 
  <t t-set="test_variable" t-value="test_variable+i"/> 
</p> 
<h1>RESULT=<t t-esc="test_variable"/></h1>
```
