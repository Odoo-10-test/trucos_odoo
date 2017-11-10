# Mensajes en Odoo

```
# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.misc import formatLang
import odoo.addons.decimal_precision as dp
from datetime import datetime
```

```
@api.onchange('discount')
    def onchange_discount_order_line(self):
        res = {}
        warning = False
        if self.discount > self.order_id.user_id.sale_max_por:
            warning = {
                    'title': _('Warning!'),
                    'message': _('El usuario %s no tiene permiso para un descuento del %d .!' %(self.order_id.user_id.name,self.discount)),
                }
            self.discount = 0
            res = {'warning': warning}
        if self.price_unit < self.product_id.standard_price:
                raise UserError('El precio del producto no puede ser menor que el costo')
        return res
```
