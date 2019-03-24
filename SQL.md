# Consultas en una línea
```
doc_class_ref_id = doc_class.search([('sii_code', '=', 'OTROS')], limit=1)
```


# Consultas en una línea
```
discount = self.product_id.discount_id.discount_ids.filtered(lambda d: d.qty <= self.product_uom_qty).sorted('qty')
```

# Consultas en Odoo
```
sale_id = fields.Many2one('sale.order', string='Orden de Venta', compute='calcular_saleorder')

    @api.one
    @api.depends('origin')
    def calcular_saleorder(self):
        if self.origin:
            obj_sale_order = self.env['sale.order'].search([('name', '=', self.origin)], limit=1)
            if obj_sale_order:
                self.sale_id = obj_sale_order[0]

```



# Consultas rápidas a Odoo
```
obj_product_product = self.env['product.product'].search([('active', '=', True)])
        for id in obj_product_product:
            # print id.name
            default_code = "-"
            if id.default_code:
                default_code = id.default_code
 ```               
                
# Consultas rápidas a Odoo
```
obj_stock_move = self.env['stock.move'].search([('state', '=', 'confirmed')])
        for id in obj_stock_move:
                print id.name
```

# Creando Valores
```
from odoo.exceptions import ValidationError



            for id in self.tag_mrp_ids:
                contador += 1
                vals = {
                    'template_id': self.product_id.id,
                    'name': id.name,
                    'tag_date': datetime.today(),
                }
                print vals
                insert = self.env['tag.list'].create(vals)

            if contador != self.product_qty:
                raise ValidationError(_("Importante! La cantidad de tags no es igual a los productos a producir"))
```



 # Creando Valores
```
  vals = {
           'product_id': id,
           'price_list_id': pricelist_report_id.id,
          }

  insert = self.env['list.product.report'].create(vals)
 ```


# Ejemplo de consulta SQL en Odoo

```
cad_short = self.default_code
                    # cad_short = "131012"
                    self.env.cr.execute("SELECT * FROM product_template  WHERE default_code LIKE '" + cad_short + "%' ")
                    if self.env.cr.rowcount:
                        res = self.env.cr.dictfetchall()
                        for fila in res:
                            mayor = 0
                            numero_correlativo = fila['default_code']
                            numero_correlativo = numero_correlativo[6:9]
                            if numero_correlativo == '':
                                numero_correlativo = '0'
                            numero = int(numero_correlativo)
                            if numero > mayor:
                                mayor = numero
 ```
 
 # Ejemplo de consulta SQL en Odoo buscando un elemento

```
contpm = 0
            numero2 = 0
            for task in order.list_task_ids:
                numero2 = numero2 + 1
                contpm = contpm + 1
                self.env.cr.execute("SELECT id FROM maintenance_tree  WHERE contador = '" + str(contp) + "'")
                if self.env.cr.rowcount:
                    parent_code = self.env.cr.fetchone()[0]
                vals3 = {'cod': "TA" + str(task.id), 'name': order.desc + " / " + task.task_id.name, 'parent_id': parent_code , 'end': task.end,
                         'numero': str(numero) + "."+ str(numero2),
                         'costo_rc': task.importe, 'costo': task.importe,
                         'type': 'TA',
                         'deadline': task.deadline,
                         'peticion': order.request_name,
                         'sector': order.sector_name,
                         'responsable': task.employee_id.name}
                self.env['maintenance.tree'].create(vals3)
 ```
 
 
 
 # Usos de CR

```
cr.dictfetchall() will give you [{'reg_no': 123},{'reg_no': 543},].
cr.dictfetchone() will give you {'reg_no': 123}.
cr.fetchall() will give you '[(123),(543)]'.
cr.fetchone() will give you '(123)'.
```

# Ejemplo de busqueda con actualización
```
@api.multi
    def run_sii_partner_update(self, exe, alias=None):
        tiempo_inicial = time()
        _logger.info('Se ha Iniciado el Proceso de Actualizacion de Contribuyente')
        contador = 1
        obj_partner = self.env['res.partner'].search([('active', '=', 'True')])
        if obj_partner:
            for id in obj_partner:
                contador = contador + 1
                if id.document_number:
                    print str(contador) + "-" +  id.document_number
                    obj_partner_sii = self.env['sii.partner'].search([('document_number', '=', id.document_number)])
                    if obj_partner_sii:
                        for id_sii in obj_partner_sii:
                            id.dte_email = id_sii.dte_email
```



# Orden
```
obj_stock_move = self.env['stock.move'].search([('picking_type_id', '=', 4), ('state', 'in', ['confirmed', 'assigned'])]).sorted('date_expected')

# ('id desc')

            consecutivo_linea_so = 1

            for id in obj_stock_move:
                if id.state == 'confirmed' or id.state == 'assigned':
                
   ``` 
   
   
# Recorrer
```
obj_product_product = self.env['product.product'].search([('active', '=', True)])
        for id in obj_product_product:
            # print id.name
            default_code = "-"
            if id.default_code:
                default_code = id.default_code

            barcode = ""
            if id.barcode:
                barcode = id.barcode
            color = ""
            numero = ""
            talla = ""
            if id.attribute_value_ids:
                # print id.attribute_value_ids
                for att in id.attribute_value_ids:
                    if att.attribute_id.name == "Color" or att.attribute_id.name == "color" or att.attribute_id.name == "COLOR":
                        color = att.name
```


