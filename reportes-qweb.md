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
