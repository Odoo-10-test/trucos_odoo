
# Fecha de Entrada
```
from datetime import datetime
entry_date = fields.Datetime('Fecha de Entrada', default = lambda self: datetime.today()) 
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
