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
