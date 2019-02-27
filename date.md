fechas Chile

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
