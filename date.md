 # Sumar Días Laborables
 ```
from odoo import api, fields, models
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)
from dateutil.relativedelta import relativedelta
try:
    import pandas as pd
    from pandas.tseries.offsets import BDay
except ImportError as exc:
	_logger.error('Faltan dependencias: %s', exc)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    days_receive = fields.Integer("Days to Receive it")

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('partner_id','order_line')
    def onchange_partner_date(self):
        if self.state == 'draft':
            if self.partner_id and self.partner_id.days_receive > 0:
                days_partner = self.partner_id.days_receive
                self.date_planned = datetime.today() + BDay(days_partner)
            else:
                self.date_planned = False
 ```

# Restart Fechas
```
@api.multi
    def _compute_giveme_day_from(self):
        for record in self:
            fecha1 = datetime.now()
            fecha2 = datetime.strptime(record.entry_date,"%Y-%m-%d %H:%M:%S")
            record.day_from_begin = abs(fecha1 - fecha2).days
 ```


# Sumar Dias a una Fechas
```
import datetime
date_1 = datetime.datetime.strptime(start_date, "%m/%d/%y")
end_date = date_1 + datetime.timedelta(days=10)
```


# Fecha de Entrada
```
from datetime import datetime
entry_date = fields.Datetime('Fecha de Entrada', default = lambda self: datetime.today())
```

# Fecha de entrada
```
start_date = fields.Date('Fecha Inicio', default=_get_default_start_date, help='Ingrese la fecha inicio del periodo')
end_date = fields.Date('Fecha Fin', default=_get_default_end_date, help='Ingrese la fecha fin del periodo')

@api.model
def _get_default_start_date(self):
    date = fields.Date.from_string(fields.Date.today())
    start = '%s-%s-01' % (date.year, str(date.month).zfill(2))
    return start
    
    
@api.model
def _get_default_end_date(self):
    date = fields.Date.from_string(fields.Date.today())
    end_of_month = monthrange(date.year, date.month)[1]
    end = '%s-%s-%s' % (date.year, str(date.month).zfill(2), end_of_month)
    return end
```
# Rango de Fechas

```
# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from datetime import *

inicio = date(2018,5,1)
fin = date(2019,2,1)

while inicio < fin:
    print inicio.strftime('%Y-%m-20')
    inicio += relativedelta(months=1)
    
```

```
2018-05-20
2018-06-20
2018-07-20
2018-08-20
2018-09-20
2018-10-20
2018-11-20
2018-12-20
2019-01-20    
```

# Rango de Fechas

```
# -*- coding: utf-8 -*-

from datetime import date
from datetime import timedelta

hoy = date.today()

for i in range(7):
    print hoy
    hoy += timedelta(days=1)
    
```

```
2019-02-27
2019-02-28
2019-03-01
2019-03-02
2019-03-03
2019-03-04
2019-03-05
```
