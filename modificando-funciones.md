# Modificando las Función de Factura cuando se valida
```
@api.multi
    def action_invoice_open(self):
        ''' Herencia de metodo original de validacion de facturas.'''
        res = super(invoice_sii, self).action_invoice_open()
        if self.type == 'in_invoice':
            # Si la empresa esta Online y existe documento XML del proveedor
            if not self.company_id.offline:
                if not self.sii_xml_data:
                    _logger.info("La factura no posee un XML asociado del cual emitir una respuesta.!")
                    return res
                # Aceptamos Xml
                if self.forma_pago == '1':
                    self.state_dte_partner = 'accepted'
                else:
                    self.accept_dte_claim()

        if self.type == 'out_invoice' and self.document_class_id.sii_code in ['33','34']:
            if not self.company_id.offline:
                self.sale_xml_email_send()

        return res
 ```
 # Modificando la Función Crear de Stock
  ```
class StockPickingSii(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, values):
        Company = self.env['res.company'].browse(values['company_id'])
        if Company.auto_gde:
            values['electronic_picking'] = True
            values['direccion_origen_id'] = Company.partner_id.id
            values['direccion_despacho_id'] = values['partner_id']
        res = super(StockPickingSii, self).create(values)
        if values['origin']:
            sale = self.env['sale.order'].search([('name','=',values['origin'])])
            if sale:
                if sale.ot_cliente:
                    doc_class_id = self.env['sii.document.class'].search([('sii_code','=','801')],limit=1)
                    references = {
                        'list_name': doc_class_id.id,
                        'list_folio': sale.ot_cliente,
                        'list_fecha':sale.odc_date,
                        #'list_tipo': sale.ot_cliente,
                        'invoice_c_id': False
                        }
                    res['referencias_ids'] = [(0, 0, references)]
                    res['note'] = str(sale.ot_cliente)+' ('+str(sale.odc_date)+')'
                    #DIRECCION DE ENTREGA: '+str(self.direccion_despacho_id.city)+' - '+str(self.direccion_despacho_id.city_id.name)
        return res
```

# Heredando una función Existente
```
@api.model
    def cron_asign_vacation_days(self):
        res = super(HolidaysSettingsVP, self).cron_asign_vacation_days()
        u""" Asigna las vacaciones pendientes a cada empleado """
        print "-----------"
        return res
```
