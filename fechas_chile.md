fechas Chile

```
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta, date
import pytz

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    number_days = fields.Integer(compute="_compute_number_days", store=False, string='Dias')

     
    def _compute_number_days(self):
        def time_now(formato='%Y-%m-%d'):
            tz = pytz.timezone('America/Santiago')
            return datetime.now(tz).strftime(formato)

        for i in self:
            a = i.date_due
            print time_now()

            print a
            if i.date_due:
                days = datetime.strptime(i.date_due, '%Y-%m-%d') - datetime.strptime(time_now(), '%Y-%m-%d')
                i.number_days = days.days
```
