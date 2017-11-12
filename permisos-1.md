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
