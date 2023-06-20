# Multicompany
```
<field name="company_id" groups="base.group_multi_company"/>
```

# Show columns
```
<field name="project_id" optional="show"/>
```

# Colors en tree view
```
<tree
                    delete="false"
                    decoration-muted="state == 'cancel'"
                    decoration-danger="state == 'draft'"
                >
```


# State and button
```
<form string="Product out" delete="false">
                      <header>
                          <button name="get_off" string="Get off" class="oe_highlight" type="object"
                             attrs="{'invisible': [('state','not in',('draft'))]}"/>

                         <field name="state" widget="statusbar"/>
                      </header>

                    <sheet>
                    ```
