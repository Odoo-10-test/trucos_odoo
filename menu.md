
# Creando Menu adicional con filtros

```
<record id="action_invoice_rejected_sii" model="ir.actions.act_window">
        <field name="name">Documentos Rechazados</field>
        <field name="res_model">account.invoice</field>
        <field name="type">ir.actions.act_window</field>
        <field name="view_type">form</field>
        <field name="view_mode">tree,form,kanban,calendar,graph,pivot</field>
        <field name="domain">[('type', 'in', ['out_invoice','out_refund']),('sii_result','=','rejected')]</field>
        <field name="search_view_id" ref="account.view_account_invoice_filter"/>
    </record>
```
