# Trucos con los data

# Cargar Datos Masivos
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <record id="001" model="tipo.comprobante">
             <field name="name">FACTURA A</field>
             <field name="codigo">001</field>
             <field name="desc">A</field>
             <field name="permitido_venta">True</field>
        </record>
    </data>
</odoo>
```

# Importar un campo many2one

```
<?xml version="1.0" encoding="utf-8"?>
  <odoo>
     <data noupdate="0">
          <record id="R1" model="condicion.venta">
               <field name="name">IVA Responsable Inscripto</field>
               <field name="codigo">1</field>
             <field name="for_company">True</field>
             <field name="for_partner">True</field>
             <field name="comprobante_ids" eval="[(4,ref('l10n_ar_base.001')),
                                             (4,ref('l10n_ar_base.002')),
                                             (4,ref('l10n_ar_base.003')),
                                             (4,ref('l10n_ar_base.004')),
                                             (4,ref('l10n_ar_base.051')),
                                             (4,ref('l10n_ar_base.011')),
                                            (4,ref('l10n_ar_base.012')),
                                             (4,ref('l10n_ar_base.013')),
                                             (4,ref('l10n_ar_base.015')),
                                             (4,ref('l10n_ar_base.052')),
                                             (4,ref('l10n_ar_base.053')),
                                             (4,ref('l10n_ar_base.054')),
                                                ]"/>
          </record>
      </data>
  </odoo>
```
