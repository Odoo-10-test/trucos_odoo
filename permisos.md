## Ejemplo de permisos en menu

```
<menuitem id="main_base_menu_dte" name="DTE" sequence="10" groups="base.group_system"/>

```

## Ejemplo de permisos

El módelo en este caso es: sales.rubro

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sales_rubro,sales_rubro,model_sales_rubro,sales_team.group_sale_salesman,1,1,1,1
access_sales_rubro,sales_rubro,model_sales_rubro,account.group_account_user,1,1,1,1
```

## Ejemplo creando Permisos
groups.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <record id="bim_manager_group" model="res.groups">
                <field name="name">Presupuesto BIM Admin.</field>
            <field name="menu_access" eval="[(4,ref('main_base_menu_bim')),]"/>
        </record>
        
        <record id="bim_user_group" model="res.groups">
            <field name="name">Presupuesto BIM Usuario</field>
            <field name="menu_access" eval="[(4,ref('main_base_menu_bim')),]"/>
        </record>
    </data>
</odoo>

```

ir.model.access.csv

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
manager_bim_account_invoice,manager.bim.account.invoice,account.model_account_invoice,bim_manager_group,1,1,1,1

user_bim_account_invoice,user.bim.account.invoice,account.model_account_invoice,bim_user_group,1,0,0,0

```
