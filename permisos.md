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
manager_bim_product_template,manager.bim.product.template,product.model_product_template,bim_manager_group,1,1,1,1
manager_bim_apu_template,manager.bim.apu.template,model_apu_template,bim_manager_group,1,1,1,1
manager_bim_construction_group,manager.bim.construction.group,model_construction_group,bim_manager_group,1,1,1,1
manager_bim_construction_sub_group,manager.bim.construction.sub.group,model_construction_sub_group,bim_manager_group,1,1,1,1
manager_bim_capitulo,manager.bim.capitulo,model_bim_capitulo,bim_manager_group,1,1,1,1
manager_bim_capitulo_presupuesto,manager.bim.capitulo.presupuesto,model_bim_capitulo_presupuesto,bim_manager_group,1,1,1,1
manager_bim_capitulo_apu,manager.bim.capitulo.apu,model_bim_capitulo_apu,bim_manager_group,1,1,1,1
manager_bim_list_materiales,manager.bim.list.materiales,model_list_materiales,bim_manager_group,1,1,1,1
manager_bim_list_control,manager.bim.list.control,model_list_control,bim_manager_group,1,1,1,1
manager_bim_list_control_obra,manager.bim.list.control.obra,model_list_control_obra,bim_manager_group,1,1,1,1
manager_bim_obra,manager.bim.obra,model_bim_obra,bim_manager_group,1,1,1,1
manager_bim_presupuesto,manager.bim.presupuesto,model_bim_presupuesto,bim_manager_group,1,1,1,1
manager_res_partner,manager.res.partner,model_res_partner,bim_manager_group,1,1,1,1
manager_res_company,manager.res.company,model_res_company,bim_manager_group,1,1,1,1
manager_load_apu_wizard,manager.load.apu.wizard,model_load_apu_wizard,bim_manager_group,1,1,1,1
manager_load_apu_wizard_line,manager.load.apu.wizard.line,model_load_apu_wizard_line,bim_manager_group,1,1,1,1

user_bim_account_invoice,user.bim.account.invoice,account.model_account_invoice,bim_user_group,1,0,0,0
user_bim_product_template,user.bim.product.template,product.model_product_template,bim_user_group,1,0,0,0
user_bim_apu_template,user.bim.apu.template,model_apu_template,bim_user_group,1,0,0,0
user_bim_construction_group,user.bim.construction.group,model_construction_group,bim_user_group,1,0,0,0
user_bim_construction_sub_group,user.bim.construction.sub.group,model_construction_sub_group,bim_user_group,1,0,0,0
user_bim_capitulo,user.bim.capitulo,model_bim_capitulo,bim_user_group,1,0,0,0
user_bim_capitulo_presupuesto,user.bim.capitulo.presupuesto,model_bim_capitulo_presupuesto,bim_user_group,1,0,0,0
user_bim_capitulo_apu,user.bim.capitulo.apu,model_bim_capitulo_apu,bim_user_group,1,0,0,0
user_bim_list_materiales,user.bim.list.materiales,model_list_materiales,bim_user_group,1,0,0,0
user_bim_list_control,user.bim.list.control,model_list_control,bim_user_group,1,0,0,0
user_bim_list_control_obra,user.bim.list.control.obra,model_list_control_obra,bim_user_group,1,0,0,0
user_bim_obra,user.bim.obra,model_bim_obra,bim_user_group,1,0,0,0
user_bim_presupuesto,user.bim.presupuesto,model_bim_presupuesto,bim_user_group,1,0,0,0
user_res_partner,user.res.partner,model_res_partner,bim_user_group,1,0,0,0
user_res_company,user.res.company,model_res_company,bim_user_group,1,0,0,0
user_load_apu_wizard_line,user.load.apu.wizard.line,model_load_apu_wizard_line,bim_user_group,1,0,0,0

```
