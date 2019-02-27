
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
