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
