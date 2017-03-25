# Trucos con los modelos

# Tipos de campos en Odoo

```
folio = fields.Integer(string='Folio:', size=10)
name = fields.Char(string='New Value', size=64, required=True)
online_mode = fields.Boolean('Online Mode', help='Si esta activo', default='True')

doc_type = fields.Selection(
            [('D','RUT Chile'),
            ('P','Pasaportes'),
            ('C ','Permiso de conducir Chile '),
            ('I','Carta o documento de identidad'),
            ('X','Permiso de residencia UE'),
            ('N','Permiso de residencia Chile ')],
            'Tipo de Documento', size=1)
            
gender = fields.Selection([('F','Femenino'),('M','Masculino')],'Sexo',size=1)
  
company_id = fields.Many2one('res.company', string='Compañía', change_default=True, readonly=True,
            default=lambda self: self.env['res.company']._company_default_get('traveler.register'))
            
entry_date = fields.Datetime('Fecha de Entrada', default = lambda self: datetime.today()) 
```

# Opciones en los campos básicos en Odoo

```
from openerp import models, fields

class AModel(models.Model):

    _name = 'a_name'

    name = fields.Char(
        string="Name",                   # Optional label of the field
        compute="_compute_name_custom",  # Transform the fields in computed fields
        store=True,                      # If computed it will store the result
        select=True,                     # Force index on field
        readonly=True,                   # Field will be readonly in views
        inverse="_write_name"            # On update trigger
        required=True,                   # Mandatory field
        translate=True,                  # Translation enable
        help='blabla',                   # Help tooltip text
        company_dependent=True,          # Transform columns to ir.property
        search='_search_function'        # Custom search function mainly used with compute
    )
```


# Funcion OnChange
```
    partner_id = fields.Many2one('res.partner','Socio')
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        partner_id = self.partner_id
        if partner_id:
            self.first_name = partner_id.name
            if not partner_id.country_id:
                raise UserError(_('Error 0001: No existe el pais'))
            self.birth_country = partner_id.country_id.id
```

# Clase
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime

class LibreDTEResCompany(models.Model):
    _inherit = "res.company"
    libredte_hash = fields.Char('LibreDTE hash', help="Code from LibreDTE")
    dte_preliminar = fields.Boolean('DTE Preliminar', help='Si esta activo enviará el dte de forma preliminar')
    online_mode = fields.Boolean('Online Mode', help='Si esta activo enviará el dte, si no está activo solo contabiliza', default='True')
```


