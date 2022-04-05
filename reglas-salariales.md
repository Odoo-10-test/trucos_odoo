 # Reglas Salariales
 ```
 NETO
 result = contract.hourly_wage * worked_days.WORK100.number_of_hours
 ```
 
 ```
 TAX
 result = NETO*0.0765
 ```
 
 
 ```
 COMISSION
 result = employee._get_commission(payslip.date_from, payslip.date_to)
 ```
  
 ```
 NET
 result = NETO - STAXD + COM
 ```
