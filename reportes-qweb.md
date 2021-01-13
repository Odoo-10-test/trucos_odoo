# Trucos de Reportes
# If else
```
<t t-if="origin != l.origin">
  <td>foo</td>
</t>
<t t-else="">
  <td>bar</td>
</t>
```

```
<td>
    <t t-if="o.opportunity_id">
        <span t-field="o.opportunity_id.user_id.code_user"/>
    </t>
   <t t-else="">
        <t t-if="o.partner_id.parent_id">
            <span t-field="o.partner_id.parent_id.user_id.code_user"/>
         </t>
    <t t-else="">
   <span t-field="o.partner_id.user_id.code_user"/>
  </t>
 </t>
</td>
```

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
