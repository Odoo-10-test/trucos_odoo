Mensajes no bloqueantes
```
@api.onchange('confirm_container')
    def _onchange_confirm_container(self):
        if self.confirm_container:
            if self.confirm_container != self.all_container.name:
                self.confirm_container = False
                return {
                    'warning': {
                        'title': "Error",
                        'message': "The container is not the same",
                    }
                }
```

OnChange
```
# onchange date_from
    @api.onchange('date_from')
    def onchange_date_from(self):
        self.date_to = self.date_from
```

Funciones lambda por defecto
```
default=lambda self: self.env.company.hourly_cost
```

Guardando un Loop en cada ciclo.
```
count += 1
if count == 100:
_logger.info('100 records created ')
self.env.cr.commit()
count = 0
```

Validando el cargar una libreria
```
_logger = logging.getLogger(__name__)
try:
    import Crypto
except (ImportError, IOError):
    _logger.warning('Missing library Crypto.')
```

```
self.ensure_one()
```

# Error de Usuario
```
from odoo.exceptions import UserError
if self.state_invoice == 'invoiced':
	raise UserError('Un albarán facturado no puede modificarse.')
```


# Importar desde excell
```
try:
    import xlrd
except (ImportError, IOError):
    plt = False
    _logger.warning('Missing library xlrd.')
    
     def import_excel_file(self):
        if not self.file:
            raise UserError("Es necesario un Fichero para Importar")
        if not self.excel_validator(self.file_name):
            raise UserError(_("File must contain excel extension"))
        self.import_lines.unlink()
        data = base64.b64decode(self.file)
        work_book = xlrd.open_workbook(file_contents=data)
        sheet = work_book.sheet_by_index(0)
        LineObj = self.env['sale.order.import.line']
        first_row = []
        last = sheet.nrows
        row_count = 0
        for col in range(sheet.ncols):
            first_row.append(sheet.cell_value(0, col))
        for count, row in enumerate(range(1, sheet.nrows), 2):
            row_count += 1
            val = {}
            for col in range(sheet.ncols):
                val[first_row[col]] = sheet.cell_value(row, col)
            vals = self._prepare_future_order_vals(val)
            LineObj.create(vals)
            print("FILA %s DE %s"%(row_count,last))
    
    
    
    
@api.model
    def excel_validator(self, xml_name):
        name, extension = os.path.splitext(xml_name)
        return True if extension in ['.xlsx','.xls'] else False

```

# Ternario
```
move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
```


# Buscamos en un tipo
```
elif line.account_id.user_type_id.type in ('receivable', 'payable'):
```
# Sumamos los subtotales
```
afecto = sum(line.price_subtotal for line in move.invoice_line_ids if line.tax_ids)
```

# Saber el nombre de la bd en odoo 14
```
ignore_db = fields.Char(default=lambda self: self.env.cr.dbname, string='Ignorar Esta Bd')

```

# Ordenar un filtro en odoo
```
    def _rectify_move_product_lines(self):
        for move in self:
            product_lines = move.line_ids.filtered_domain([('tax_line_id','=',False),('account_internal_type','=','other')])
            credit = sum(line.credit for line in product_lines)
            debit = sum(line.debit for line in product_lines)
            if move.move_type in ['out_invoice','in_refund']:
                if credit != move.amount_untaxed:
                    amount = move.amount_untaxed - credit
                    move._helper_product_asset_rectification('credit', amount,product_lines)
            elif move.move_type in ['in_invoice', 'out_refund']:
                    amount = move.amount_untaxed - debit
                    move._helper_product_asset_rectification('debit', amount,product_lines)
```                 

Exportar a exell
```
import xlwt

wb = xlwt.Workbook()
ws = wb.add_sheet('Report')
ws.write(0,0, '0 here')
ws.write(43,12, '12 here')
ws.horz_page_breaks = [(44,0,12),]
wb.save('sample.xls')
```


# Crear Albaran
```
      def action_create_picking_from_ware_house(self):
        if not self.sale_id.location_dest_id:
            raise UserError('You have to define a Temporal Location for this Sale before you receive from Warehouse')
        moves = []
        for line in self.lines_ids:
            if line.product_id.type in ['consu', 'product']:
                    moves.append((0, 0, {
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.qty_to_transfer,
                        'product_uom': line.product_id.uom_id.id,
                        'name': line.product_id.name,
                        'quantity_done': line.qty_to_transfer,
                    }))
                    if self.transfer_location_type == 'internal':
                        line.sale_line_id.internal_warehouse_qty = line.sale_line_id.internal_warehouse_qty - line.qty_to_transfer
                    else:
                        line.sale_line_id.external_warehouse_qty = line.sale_line_id.external_warehouse_qty - line.qty_to_transfer
                    line.sale_line_id.received_qty = line.sale_line_id.received_qty + line.qty_to_transfer
        if moves:
            picking_type = self.env['stock.picking.type'].search(
                [('code', '=', 'internal'), ('company_id', '=', self.sale_id.company_id.id)],
                limit=1)
            if self.transfer_location_type == 'internal':
                whare_house_location = self.env.company.location_dest_internal_id
            else:
                whare_house_location = self.env.company.location_dest_external_id

            if not picking_type:
                raise UserError(
                    'There is not Internal Operation Types defined for this Company.')

            picking = self.env['stock.picking'].create({
                'picking_type_id': picking_type.id,
                'origin': self.sale_id.name,
                'move_lines': moves,
                'location_id': whare_house_location.id,
                'sale_id_for_warehouse': self.sale_id.id,
                'location_dest_id': self.sale_id.location_dest_id.id,
                'partner_id': self.sale_id.partner_id.id,
                'company_id': self.env.user.company_id.id,
                'scheduled_date': fields.Date.today().strftime('%Y-%m-%d'),
            })
            picking.action_confirm()
            picking.action_assign()
            picking.button_validate()
            picking.create_automatic_stock_move_log('Transferencia de salida de Taller', self.sale_id, False)
            msg = (
                "Creada Transferencia: {} de producto desde la Ubicación del Taller: {} hacia la Ubicación: {} del pedido: {} por usuario: {}.<br>").format(
                picking.name, whare_house_location.name, self.sale_id.location_dest_id.name, self.sale_id.name, self.env.user.name)
            self.sale_id.message_post(body=_(msg))
```


# Crear factura desde venta
```
def action_invoice_sale_advanced(self, sale_flow):
        invoice_obj = self.env['account.move']
        vals = self._prepare_invoice_sale()
        invoice = invoice_obj.sudo().create(vals)
        invoice.sudo().action_post()
        if sale_flow == 'payment':
            self.action_payment(invoice)

    def _prepare_invoice_sale(self):
        self.ensure_one()
        vals = self._prepare_invoice()
        for line in self.order_line:
            account = False
            try:
                accounts = line.product_id.product_tmpl_id.get_product_accounts()
                if type in ('out_invoice', 'out_refund'):
                    account = accounts['income'].id
                else:
                    account = accounts['expense'].id
            except:
                pass
            line_vals = line._prepare_invoice_line()
            line_vals.update({'account_id': account})
            vals['invoice_line_ids'].append(
                (0, 0,line_vals))
        return vals
```

# Property
```
property_warehouse_id = fields.Many2one('stock.warehouse', company_dependent=True, string="Almacén")
```


# Precio calculado en base a tarifa
```
product_price = self.pricelist_id.get_product_price(self.product_id, quantity=1, self.partner_id,
                                                                    uom_id=self.product_id.uom_id.id)
```

# sql_constraints
```
_sql_constraints = [
        ('name_uniq', 'unique(variable)',
         _('La Variable debe ser única')),
    ]
```

# Etiquetas
```
category_id = fields.Many2many('res.partner.category', column1='partner_id',
                                    column2='category_id', string='Tags', default=_default_category)
				    
<field name="category_id" optional="hide" widget="many2many_tags" options="{'color_field': 'color'}"/>
```				    


```
    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        print(self._context)
        print(fields)
        if self._context.get('params'):
            if self._context.get('params').get('id'):
                sale = self.env['sale.order'].browse(self._context['params']['id'])
                res['reseller_id'] = sale.partner_id.reseller_id.id
        return res

    @api.model
    def create(self, values):
        res = super().create(values)
        print(self.partner_id)
        return res

    @api.onchange('partner_id')
    def onchange_partner_pro_id(self):
        print(self.partner_id)
```

# Sumando Hijos
```
amount_total = fields.Float('Importe' , compute='_compute_amount_total')

    @api.depends('product_ids')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum( i.importe for i in record.product_ids)
```


# Default
```
@api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self.env.user.user_sale_note:
            res['note'] = res['note'] + self.env.user.user_sale_note
        return res
```

# Nunca Hagas esto
```
for i in tasks:
   self.env['res.users'].search([])
   ```

# Saber si un modulo esta instalado
```
if 'point_of_sale' in self.env.registry._init_modules:
```


# Atributo track_visibility por tracking True|False.
```
attributable_to_state = fields.Float(string='[65] % attributable to State', default=100, tracking=True)
```

# Buscar el ultimo día del mes anterior
```
import datetime as dt
creation_date = fields.Date(string="Created On", default= dt.date.today().replace(day=1)+dt.timedelta(days=-1))
```

# creation_date
```
creation_date = fields.Date(string="Created On", default=fields.Date.context_today)
```

# Compute Inverse
```
seller_price = fields.Float("Precio Compra", compute='_compute_seller_price', inverse='_inverse_seller_price')

    @api.depends('variant_seller_ids')
    def _compute_seller_price(self):
        for record in self:
            seller_price = 0
            cont = 0
            obl_line = record.env['product.supplierinfo'].search([('product_id', '=', record.id)],limit=1)
            if obl_line:
                for line in obl_line:
                    if cont == 0:
                        seller_price = line.price
                    cont += 1
                record.seller_price = seller_price

    def _inverse_seller_price(self):
        for record in self:
            obl_line = record.env['product.supplierinfo'].search([('product_id', '=', record.id)],limit=1)
            if obl_line:
                obl_line.price = record.seller_price
```


# Action show_form_product
```
<field name="product_template_attribute_value_ids" position="after">
                <button name="show_form_product" string="Show" class="oe_highlight" type="object"/>
            </field>
	    
	    
	    
    def show_form_product(self):
        action = self.env["ir.actions.actions"]._for_xml_id("product.product_normal_action_sell")
        form_view = [(self.env.ref('product.product_normal_form_view').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = self.id
        action['views'] = form_view
        return action	    
```

# Create
```
@api.model
    def create(self, values):
        res = super().create(values)
        sale = self.create_sale_orders(values, res.id)
        return res
```

# search
```
# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)
from odoo.osv import expression

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args = expression.normalize_domain(args)
        for arg in args:
            if isinstance(arg, (list, tuple)) and (
                    arg[0] == "name" or arg[0] == "display_name"
            ):
                index = args.index(arg)
                args = (
                        args[:index] + ["|", ("origin", arg[1], arg[2])] + args[index:]
                )
                break
        return super().search(
            args, offset=offset, limit=limit, order=order, count=count
        )
```

# name_search
```
from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('origin', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()
```



# AttributeError: 'NoneType' object has no attribute 'something'
```
# you can avoid some of these error by adding this kind of check
if(x1 is not None):
    ... Do something here
else:
    print("X1 variable is Null or None")
```


# Domain OR + AND + OR
```
['|', ('user_id', '=', uid), '&', ('lang', '!=', 'fr_FR'), '|', ('phone', '=', False), ('email', '=', False)].
```


# Notificación
```
@api.multi
    def button_validate(self):
        self.env.user.notify_warning('Por favor, revisa que las cantidades son las correctas.')
        res = super(StockPicking, self).button_validate()
        return res
```


# Vals
# Lista de de Dominios de Operadores.
```
    @api.model
    def create(self, vals):
        if 'sale_api_origin' in vals:
            sale_api_obj = self.env['sale.api'].search([('id', '=', vals['sale_api_origin'])])
            vals['company_id'] = sale_api_obj.company_id.id
            if vals.get('name', _('New')) == _('New'):
                if 'company_id' in vals:
                    vals['name'] = self.env['ir.sequence'].with_context(force_company=sale_api_obj.company_id.id).next_by_code(
                        'sale.order') or _('New')
                else:
                    vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')
        result = super(SaleOrder, self).create(vals)
        return result
```

# Lista de de Dominios de Operadores.
```
List of Domain operators: ! (Not), | (Or), & (And)

List of Term operators: '=', '!=', '<=', '<', '>', '>=', '=?', '=like', '=ilike', 'like', 'not like', 'ilike', 'not ilike', 'in', 'not in', 'child_of'
```

# Campos Default Funciones
```
    def _get_default(self):
        line = self.env['sale.order.line'].search([('id', '=', self._context.get('active_id'))])
        product_id = line.product_id.product_tmpl_id.id
        partner_id = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', product_id)], limit=1).name.id
        return partner_id

    partner_id = fields.Many2one('res.partner', 'Proveedor', required=True ,default=_get_default)
```


# Saber si un módulo esta Instalado.
```
if 'l10n_es_aeat_sii' in self.env.registry._init_modules:
```

# get_param
```
 email_exchange_system = fields.Char(
        "Exchange System Email Address",
        help="The first time you send a PEC to SDI, you must use the address "
             "sdi01@pec.fatturapa.it . The system, with the first response "
             "or notification, communicates the PEC address to be used for "
             "future messages",
        default=lambda self: self.env['ir.config_parameter'].get_param(
            'sdi.pec.first.address')
    )
```

# Many2one
```
company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self:
        self.env['res.company']._company_default_get('sdi.channel'))
```

# One2many
```
child_ids = fields.One2many(
        string='Children Categories',
        comodel_name='medical.pathology.category',
        inverse_name='parent_id',
        domain="[('code_type_id', '=', code_type_id)]",
    )
```

# _check_recursion
```
@api.multi
    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_(
                'You are attempting to create a recursive category.'
            ))
```


# Picking Type
```
stock_asig_id = fields.Many2one('stock.picking',
                                    'Picking Asignado',
                                    domain="[('picking_type_code', '=', 'incoming')]",
                                    copy=False)
``` 


# Domain, States
``` 
partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

``` 
# Notificaciones de Odoo ERP
``` 
1- Mensaje
2- Título
3- Si es True se queda pegado

@api.model
    def create(self, vals):
        res = super(CrmPhonecall, self).create(vals)
        if res.called:
            res.user_id.notify_warning(res.name,res.partner_phone, False)
        return res
``` 

# Sql Constraints
``` 
_sql_constraints = [
        ('qty_positive', 'check (product_qty > 0)', 'The quantity to produce must be positive!'),
    ]
``` 

# Log
```  
import logging
_logger = logging.getLogger(__name__)


_logger.info('Not be found data to update the currency %s!', currency.name)
    
```   

# Compras
```  
obj_purchase = self.env['purchase.order.line'].search([('state', '=', 'purchase'),('product_id', '=', record.product_id.id)])
purchase_sum = sum(item.product_qty for item in obj_purchase)
```    
  
  ```  
  try:
  	droplet.create()
  except Exception as e:
        print('Err: {}'.format(e))
        UserError(e)
	```  

```  
```  
cost = sum(x.rule * x.list_price for x in apu.apu_template_lines if x.product_template_id.resource_type == 'M')
```  


# SQl
```  
_sql_constraints = [
        ('sale_prefix_uniq', 'unique(sale_prefix)',
         "A backend with the same sale prefix already exists")
    ]
    
``` 

# Help
```  
sale_prefix = fields.Char(
        string='Sale Prefix',
        help="A prefix put before the name of imported sales orders.\n"
             "For instance, if the prefix is 'mag-', the sales "
             "order 100000692 in Magento, will be named 'mag-100000692' "
             "in Odoo.",
    )
    
```  

# Try

```  
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


@api.multi
    def synchronize_metadata(self):
        try:
            for backend in self:
                for model_name in ('magento.website',
                                   'magento.store',
                                   'magento.storeview'):
                    # import directly, do not delay because this
                    # is a fast operation, a direct return is fine
                    # and it is simpler to import them sequentially
                    self.env[model_name].import_batch(backend)
            return True
        except Exception as e:
            _logger.error(ustr(e))
            raise UserError(
                _("Check your configuration, we can't get the data. "
                  "Here is the error:\n%s") %
                ustr(e))
```  


# Buscar un Valor con un SELF
```  

@api.depends('variant_seller_ids')
    def _compute_purchase_price(self):
        for record in self:
            record.purchase_price = record.variant_seller_ids and record.variant_seller_ids[0].price
```      


# Buscar un Valor con un SELF
```  
picking_type = self.env['stock.picking.type'].browse(picking_type_id)
```  

# Enviar un email
```  
# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = ['crm.lead']

    @api.model
    def create(self, vals):
        lead = super(CrmLead, self).create(vals)
        email_to = self.env['ir.config_parameter'].sudo().get_param('email_crm_notification')
        try:
            self.env['mail.mail'].sudo().create({
                'body_html': vals['description'],
                'subject': 'CRM Contact: %s' % vals['name'],
                'email_from': vals['email_from'],
                'email_to': email_to,
                'auto_delete': True,
            }).send()
        except:
            pass

        return lead
```  


# Format RUT
```  
def format_rut(rut):
    rut = rut.replace(".","").replace(",","").replace("-","")
    return rut[:-7] +"." + rut[-7:-4] +"." +  rut[-4:-1] +"-" + rut[-1:]
```  

# Modificando el Validar de la Factura
```  
    @api.multi
    def action_invoice_open(self):
        ''' Herencia de metodo original de validacion de facturas.'''
        res = super(AccountInvoice, self).action_invoice_open()

        # Actualiza estatus de facturacion del pedido de compra relacionado a una factura
        if self.type == 'in_invoice':
            for line in self.invoice_line_ids:
                if line.product_id:
                    if line.product_id.
        return res
```  

# Many2One Valor por defecto
```  
default= lambda s: s.env['modelo'].search([], limit=1)
```  

# Saber si un modulo esta instalado
```  

if 'mrp' in self.env.registry._init_modules:
                            if self.product_id.bom_count > 0:
```  


# Enviar un mensaje a un canal en odoo
```  
  
  def send_to_channel(self,body):
        ch_obj = self.env['mail.channel']
        ch = ch_obj.sudo().search([('name','ilike','general')])

        body_ok = body

        ch.message_post( attachment_ids=[], body=body_ok,
                         content_subtype='html', message_type='comment',
                         partner_ids=[], subtype='mail.mt_comment')
        return True
```  

# Cantidad de stock en una Ubicación
```
available_qty = product.with_context({'location' : self.source_location.id}).qty_‌ available
```

# Trucos con los modelos
```
        if period:
            period_name = fields.Date.from_string(str(period.name))
            hasta_date = fields.Date.from_string(str(vals['date']))
            if period.do_not_settle and period_name >= hasta_date:
                raise UserError('No puede asentar un Asiento en una fecha que esta cerrada contablemente !!!')
        return super(AccountMove, self).create(vals)
```

# Parametros

```
advance_payment = fields.Boolean(compute='_compute_giveme_advance_payment')

    @api.multi
    def _compute_giveme_advance_payment(self):
        adv_var = self.env['ir.config_parameter'].sudo().get_param('advance.payment')
        if adv_var == 'True':
            self.advance_payment  = True
        else:
            self.advance_payment = False
```

# One2many or Many2many 
```
 
 Agregar
 [(4, line.product_id.supplier_taxes_id.id)]
 
 
 Remplazar
 [(6,0,[line.product_id.supplier_taxes_id.id])]
 
```


# Estados
```
RO_STATES = {'draft': [('readonly', False)]}

class HrHourReport(models.Model):
    _name = 'hr.hour.report'
    _description = 'Hoja de Bonos RRHH'
    _inherit = ['mail.thread']
    _order = 'date_issue desc, name desc, id desc'
    
    line_ids = fields.One2many('hr.bonus.line', 'sheet_id', 'Bonos', readonly=True, states=RO_STATES)
```



# Fecha actual
```
date = fields.Date('Fecha contable', default=fields.Date.today)
```

# Cadenas
```
cadena = cadena + u" Socio de Negocio: %s \n"%(socio_negocio)
cadena = notas + '\n' + u" NV: %s \n" % (nv)
```


# Delete
```
alarm_ids = fields.Many2many('calendar.alarm', 'calendar_alarm_calendar_event_rel', string='Reminders', ondelete="restrict", copy=False)
```

# Evita Borrar si tiene valores
```
alarm_ids = fields.Many2many('calendar.alarm', 'calendar_alarm_calendar_event_rel', string='Reminders', ondelete="restrict", copy=False)

CASCADE: Delete the Course record with matching student_id when Student is deleted

RESTRICT: Cannot delete the Student as long as it is related to a Course.

NO ACTION: similar, but is a deferred check: You can delete the Student but you have to make sure that the integrity is OK when the transaction is committed.

SET DEFAULT: uses openerp default definition (see _defaults dict in the python model definition)

SET NULL: when a Student gets deleted, the student_id becomes NULL in the DB.
 
```


# Colocando secuencia a una vista tree
```
sequence = fields.Integer(compute='_compute_sequence')

    @api.multi
    def _compute_sequence(self):
        for i, record in enumerate(self.sorted('id', reverse=True), 1):
            record.sequence = i
```	    
	    
# Parametros
```
limit_day = self.env['ir.config_parameter'].sudo().get_param('cancel.sale.order')
```

# Utilizacion de Mappeed
```
stock = sum(locations.with_context({'template_id': record.id}).mapped('virtual_available'))
```

# Importar Correctamente una Libreria PY
```
try:
	import barcode
	from barcode.writer import ImageWriter
except ImportError as exc:
	_logger.error('Faltan dependencias: %s', exc)
``` 

# Trabajos con Fechas
```
from datetime import datetime, timedelta

@api.one
    @api.depends('desde_date', 'hasta_date')
    def _calcular_si_es_mes(self):
        hoy = datetime.now().date()
        desde = self.desde_date
        fecha_desde = datetime.strptime(str(desde), '%Y-%m-%d')
        if str(fecha_desde) < str(hoy):
            if self.hasta_date:
                hasta_date = datetime.strptime(str(self.hasta_date), '%Y-%m-%d')
                if str(hasta_date) > str(hoy):
                    self.del_mes = True
            else:
                self.del_mes = True
        else:
            self.del_mes = False
```
    
# Campos tipo moneda
```
amount_total = fields.Monetary('Total')
```


# Raise
```
from odoo.exceptions import UserError

raise UserError(_('%s no tiene contrato para el periodo %s - %s') % (employee.display_name, date_from, date_to))

raise UserError(_('El monto por préstamos no coincide:\nCuotas por pagar: %f\nMonto préstamo en nómina: %s') % (round(total_cuotas), round(total_prestamos)))

```	

# Log en campos de estados
```
state = fields.Selection([('pending', 'Pendiente'), ('error', 'Errores')], 'Estado', required=True, track_visibility='onchange')
```

# Crear como admin
```
insert = self.env['tag.list'].sudo().create(vals)
```

# Tratando de Importar una libreria
```
try:
    import pysftp
except ImportError:
    raise ImportError('This module needs pysftp to automaticly write backups to the FTP through SFTP. Please install pysftp on your system. (sudo pip install pysftp)')
 ``` 
 
 # Fecha - Today
```
from datetime import datetime
a = datetime.today()
 ``` 
 
 
 # Redefiniendo Métodos
```
 @api.multi
    def button_mark_done(self):
        if not self.tag_mrp_ids:
            raise ValidationError(_("Importante! Por favor defina los tags"))
        res = super(MrpProduction, self).do_transfer()
        return res
  ``` 
 
 # Parametros
 ```
<?xml version="1.0"?>
<odoo>
    <data noupdate="0">
    	<record id="login_form_disable_footer" model="ir.config_parameter">
            <field name="key">login_form_disable_footer</field>
            <field name="value">False</field>
        </record>
    </data>
</odoo>
 ```  
```
cr = request.cr
uid = odoo.SUPERUSER_ID
param_obj = request.env['ir.config_parameter']

change_background = ast.literal_eval(param_obj.get_param('login_form_change_background_by_hour')) or False
config_login_timezone = param_obj.get_param('login_form_change_background_timezone')
 ```  
 
 
 # Error
```
from odoo.exceptions import ValidationError
raise ValidationError(_("Importante! Por favor defina los tags"))
 ```  
 
 
 
# Herencia en el modelo
```
class SaleOrderNotCopy(models.Model):
    _inherit = "sale.order"
    user_id = fields.Many2one('res.users', copy=False)
 ```  

    
# Obtener datos desde la compañía
```
self.env.user.company_id.name
```

# Stock de un producto
```
stock = sum(id.stock_quant_ids.mapped('qty'))
```


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

# Colocando Valores por defecto

```
@api.model
    def create(self, vals):
        vals['property_payment_term_id'] = 1
        return super(res_partner_cnp, self).create(vals)
  ```      

# Salto de linea
```
'comment': note and note_sale+'\n'+note or note_sale
```

# Cadenas
```
 cadena = u" Dir. Intermediaria: %s, %s \n Dir. Final: %s, %s "%(direccion_1,ciudad,direccion_2,ciudad2)
 ```
 # Redondear con mas decimales
```
 
 monto = fields.Float('Monto', digits=(10, 4))
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


# Calculado comision en la factura
```
total = 0
for line in self.invoice_line_ids:
    if line.product_id:
        total += (line.product_id.sale_commission or 0.0) / 100.0 * line.price_unit * line.quantity
self.sale_commission = total
```


# Clase Inicial Modelo Herencia
```
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime

class LibreDTEResCompany(models.Model):
    _inherit = "res.company"
    libredte_hash = fields.Char('LibreDTE hash', help="Code from LibreDTE")
    dte_preliminar = fields.Boolean('DTE Preliminar', help='Si')
    online_mode = fields.Boolean('Online Mode', help='Si', default='True')
```

# Clase Inicial Modelo Herencia
```
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record model="ir.ui.view" id="webfactura_view_company_inherit_form">
        <field name="name">webfactura.view.company.inherit.form</field>
        <field name="inherit_id" ref="base.view_company_form"/>
        <field name="model">res.company</field>
        <field name="arch" type="xml">
            <notebook>
                <page string="LibreDTE">
                    <group cols="4">
                        <field name="libredte_hash" password="True" class="oe_inline" required="1"/>
                        <field name="dte_preliminar" />
                        <field name="online_mode" />
                    </group>
                </page>
            </notebook>
        </field>
    </record>
</odoo>
```

# Herencia de campo

```
<?xml version="1.0" encoding="UTF-8"?>
 <odoo>
    <data>
        <record model="ir.ui.view" id="partner_instructor_form_view">
            <field name="name">partner.instructor</field>
            <field name="model">res.partner</field>
            <field name="inherit_id" ref="base.view_partner_form"/>
            <field name="arch" type="xml"> 
               <field name="category_id" position="after" >          
                    <field name="rut" string="RUC:" placeholder="00000000" />
                    <field name="mail" string="Correo"/> 
               </field>                       
            </field>
        </record>
    </data>
</odoo>

```

# Clase Inicial Modelo
```
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class rrhh_afp(models.Model):
    _description = "AFP Fondo de Pension"
    _name = 'rrhh.afp'

    codigo = fields.Char('Codigo', required=True)
    name = fields.Char('Name', translate=True)
    rut = fields.Char('Rut', translate=True)
    tasa = fields.Float('Tasa', required=True)
    sis = fields.Float('Aporte Empresa', required=True)
    independiente = fields.Float('Independientes', required=True)
```

# Clase Inicial Vista
```
<?xml version="1.0" encoding="UTF-8"?>
 <odoo>
    <data>

    <record id="view_form_rrhh_afp" model="ir.ui.view">
             <field name="name">view.form.rrhh.afp</field>
             <field name="model">rrhh.afp</field>
             <field name="arch" type="xml">
                <form string="Listado de AFP">
                  <sheet>
                    <legend>AFP</legend>
                       <group>
                          <group>
                             <field name="rut"/>
                             <field name="name"/>
                             <field name="codigo"/>
                             <field name="tasa"/>
                             <field name="sis"/>
                             <field name="independiente"/>
                          </group>
                       </group>
                   </sheet>
                </form>
            </field>
    </record>

    <record id="view_tree_rrhh_afp" model="ir.ui.view">
             <field name="name">view.tree.rrhh.afp</field>
             <field name="model">rrhh.afp</field>
             <field name="arch" type="xml">
                <tree>
                             <field name="rut"/>
                             <field name="name"/>
                             <field name="codigo"/>
                </tree>
            </field>
    </record>

    <record id="action_rrhh_afp" model="ir.actions.act_window">
            <field name="name">AFP</field>
            <field name="res_model">rrhh.afp</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
              <p class="oe_view_nocontent_create">
                Presione para crear nuevo Registro</p>
           </field>
    </record>

    <menuitem id="rrhh_afp_menu"
        name="AFP"
        parent="menu_payroll_config"
        sequence="31"
        action="action_rrhh_afp" />

     </data>
</odoo>
```

# Cargar Datos
```
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data noupdate="1">
        <record id="rrhh_afp_01" model="rrhh.afp">
            <field name="name">Capital</field>
            <field name="rut">00000000-0</field>
            <field name="codigo">34</field>
            <field name="tasa">11.44</field>
            <field name="sis">1.41</field>
            <field name="independiente">12.85</field>
        </record>
        <record id="rrhh_afp_02" model="rrhh.afp">
            <field name="name">Cuprum</field>
            <field name="rut">00000000-0</field>
            <field name="codigo">03</field>
            <field name="tasa">11.48</field>
            <field name="sis">1.41</field>
            <field name="independiente">12.89</field>
        </record>
    </data>
</odoo>
```
# Ejemplo de manifest
```
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2017 Marlon Falcón Hernandez
#    (<http://www.falconsolutions.cl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Base Chilean location MFH',
    'version': '10.0.0.1.0',
    'author': "Falcón Solutions, Luis Torres...",
    'maintainer': 'Falcon Solutions',
    'website': 'http://www.falconsolutions.cl',
    'license': 'AGPL-3',
    'category': 'Localization/Chile',
    'summary': 'Chilean location: Load basic data.',
    'depends': [
                'base',
                'base_vat',
                'product',
                'account_accountant',
                ],
    'external_dependencies': {
                'python': [
                            'M2Crypto',
                            'elaphe',
                            'cchardet',
                            'rsa'
                            ],
     },
    'description': """
Módulo basado en localización Chilena
=====================================================
1-. Add SII Economical Activities.\n
2.- Load data Counties.\n
3.- Load default value in the country field in view of company and partners.\n
4.- Add Ubication field in view of company and partners.\n
5.- Incorporate a field with the RUT (VAT) formatted according chilean customs.\n
6.- This module validates the RUT directly.\n
""",
    'data': [
            'views/base_view.xml',
            'views/economical_activities.xml',
            'report/report_invoice.xml',
            'data/email_template.xml',
            'views/res_partner.xml',
            'data/uom_data.xml',
            ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,

}
```

# Campo Many2one
```
functional_area_id = fields.Many2one('functional.area', 'Areas Funcionales')
```

# Ocultar campo en la vista que depende de otro
```
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record model="ir.ui.view" id="stock_picking_inherit_form">
        <field name="name">stock.picking.inherit.form</field>
        <field name="inherit_id" ref="stock.view_picking_form"/>
        <field name="model">stock.picking</field>
        <field name="arch" type="xml">
            <field name="partner_id" position="after" >
                    <field name="electronic_picking" />
                      <field name="patente" placeholder="AA0000" attrs="{'invisible': ['|',('electronic_picking', '=', False)]}"/>
            </field>
        </field>
    </record>
</odoo>
```

# Conocer el ID
```
var = self.env['res.country'].search([('name','=','Chile')])
        self.fax = var.id
```

# Campos relacionados
```
online_mode_f = fields.Boolean('Online', related='company_id.online_mode')
```

```
 <field name="team_id" position="after" >
    <field name="online_mode_f" invisible="1" />
    <field name="number_folio" attrs="{'invisible':[('online_mode_f','=', True)]}"/>
</field>
```

# Log odoo
```
import logging
```

```
_logger.info('Not be found data to update the currency %s!',currency.name)
```


# Exportación TXT
```
@api.multi
    def download_txt(self):
        res = {}
        op = self.operation == 'sale' and 'VENTAS' or 'COMPRAS'
        fname = '%s_%s_%s_Comprobantes.txt' %(self.company_id.cuit,self.period.replace('-','_'),op)
        path = '/tmp/' + fname
        txtFile = open(path, 'wb')
        for invoice in self.invoice_ids:
            line = ''
            partner = invoice.partner_id.parent_id and invoice.partner_id.parent_id or invoice.partner_id
            line+= invoice.date_invoice.replace("-", '') #fecha factura
            txtFile.write(self.clean_accents(line)+'\n')
        txtFile.close()
        data = base64.encodestring(open(path, 'r').read())
        attach_vals = {'name': fname, 'datas': data, 'datas_fname': fname}
        doc_id = self.env['ir.attachment'].create(attach_vals)
        res['type'] = 'ir.actions.act_url'
        res['target'] = 'new'
        res['url'] = "web/content/?model=ir.attachment&id=" + str(
            doc_id.id) + "&filename_field=datas_fname&field=datas&download=true&filename=" + str(doc_id.name)
        return res

# Campo autocalculados
```
    estimado = fields.Float('Estimado')
    pagado = fields.Float('Pagado')
    restante = fields.Float(compute='calcular_restante')

    @api.one
    @api.depends('estimado','pagado')
    def calcular_restante(self):
        self.restante = self.estimado - self.pagado
 ```
 
 
 
# Crear una Secuencia
En el modelo
```
name = fields.Char('Código', translate=True, default="Nuevo")
@api.model
    def create(self, vals):
        if vals.get('name', "Nuevo") == "Nuevo":
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.haberesydesc') or "Nuevo"
        return super(hr_haberesydesc, self).create(vals)
```
En data
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="seq_hr_haberesydesc" model="ir.sequence">
            <field name="name">Haberes y Descuentos</field>
            <field name="code">hr.haberesydesc</field>
            <field name="prefix">HD</field>
            <field name="padding">5</field>
            <field name="company_id" eval="False"/>
        </record>
    </data>
</odoo>
```

# Crear valores por defecto en Campos

```
pass_cert = fields.Char('Llave Privada', help="Ruta absoluta del archivo que contiene la llave privada (.key)",
                                default="/opt/odoo/certificados/ghf.key")
```



# Validar campos antes de guardar la factura


```

from odoo.exceptions import ValidationError


    @api.constrains('name')
    def _check_codigo_point_sales(self):
        if len(self.name) < 4:
            raise ValidationError("El Punto de Venta tiene que tener 4 dígitos")
```

# Recorrer un campo many2one
```
    @api.onchange('rh_cargas_ids')
    def onchange_cargas(self):
        c_familiar = 0
        for cargas in self.rh_cargas_ids:
            if cargas.list_tipo == '1':
                c_familiar = c_familiar + 1
        self.cant_carga_familiar = c_familiar
```

# Validar antes de guardar
```

@api.constrains('name')
    def _check_codigo_point_sales(self):
        if len(self.name) < 4:
            raise ValidationError("El Punto de Venta tiene que tener 4 dígitos")
            
```

# LLamar a un metodo de otro modelo 
```
 self.env['modelo.llamar']._metodomodelo()
            
```
# LLamar a un metodo si cargamos una vista
```
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        self.env['maintenance.work.order']._check_work_order_id()
        print "Hello"
        return super(maintenance_tree, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                        submenu=submenu)
            
```

# LLamar a compañia          
```
company_id = fields.Many2one('res.company', string="Company", required=True,
                                 default=lambda self: self.env.user.company_id.id)
                                             
```
# LLamar a logo en qweb        
```

<img t-if="o.company_id.logo" t-att-src="'data:image/png;base64,%s' % o.company_id.logo"
                                style="max-height:170px; width:auto; margin:10px;"/>
                                
```
                                
# Cambiar Nombre
```
@api.multi
    def name_get(self):
        res = super(res_partner, self).name_get()
        result = []
        for element in res:
            partner_id = element[0]
            rut = self.browse(partner_id).document_number
            name = rut and '[%s] %s'%(rut,element[1]) or '%s'%element[1]
            result.append((partner_id,name))
        return result
```

# Recorrer Modelos Ejemplo Facturas
```
        invoice_obj_out_invoice = self.env['account.invoice'].search([('type','=','out_invoice')])
        for id in invoice_obj_out_invoice:
            iva_debito_fiscal = iva_debito_fiscal + id.amount_tax
 ```
 
 
 # Uso de periodos de fechas y recorrerlos
 ```
 
        invoice_obj = self.env['account.invoice']

        date = datetime.strptime(self.date, '%Y-%m-%d')
        end_of_month = monthrange(date.year, date.month)[1]
        start_period = '%s-%s-01' % (date.year, date.month)
        end_period = '%s-%s-%s' % (date.year, date.month, end_of_month)

        invoice_obj_out_invoice= invoice_obj.search([
            ('state', 'in', ['open', 'paid']),
            ('type', '=', 'out_invoice'),
            ('date_invoice', '>=', start_period),
            ('date_invoice', '<=', end_period)
        ])

        invoice_obj_in_invoice = invoice_obj.search([
            ('state', 'in', ['open', 'paid']),
            ('type', '=', 'in_invoice'),
            ('date_invoice', '>=', start_period),
            ('date_invoice', '<=', end_period)
        ])


        # Facturas de Ventas
        # invoice_obj_out_invoice = self.env['account.invoice'].search([('type','=','out_invoice')])
        for id in invoice_obj_out_invoice:
            iva_debito_fiscal = iva_debito_fiscal + id.amount_tax
 ```
  
        
# Crear log
 ``` 
self.message_post(body=_("Se ha enviado un mensaje a " + cto + ": " + ctext))

```

# BD
 ``` 

[databases]
* = host=jamoXXX.cr2z2c7klykx.eu-west-1.rds.amazonaws.com port=5432 user=dbadmin password=XXXXX

[pgbouncer]
;logfile = /var/log/postgresql/pgbouncer.log
pidfile = /var/run/postgresql/pgbouncer.pid
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = trust
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
server_reset_query = DISCARD ALL
server_check_query = select 1
server_check_delay = 10
max_client_conn = 10000
default_pool_size = 20
log_connections = 1
log_disconnections = 1
ignore_startup_parameters = extra_float_digits
server_idle_timeout = 240
admin_users = dbadmin
stats_users = dbadmin
 ```       
 
 
 # Codigo Lindos
 ```
 # coding: utf-8
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    amount_total = fields.Float('Monto total', compute='_compute_amount_total')

    @api.depends('product_id', 'product_uom_qty', 'picking_id.sale_id', 'picking_id.picking_type_id.code')
    def _compute_amount_total(self):
        po_line_obj = self.env['purchase.order.line']
        for move in self:
            if move.picking_id.picking_type_id.code == 'incoming':
                order_line = po_line_obj.search([('order_id.name', '=', move.picking_id.origin), ('product_id', '=', move.product_id.id)], limit=1)
            elif move.picking_id.sale_id:
                order_line = move.picking_id.sale_id.order_line.filtered(lambda ol: ol.product_id == move.product_id)
                if len(order_line) > 1:
                    order_line = order_line[0]
            else:
                order_line = po_line_obj
            # order_line.price_subtotal  = Precios Netos
            # order_line.price_total  = Precios Brutos
            qty_field = 'product_qty' if move.picking_id.picking_type_id.code == 'incoming' else 'product_uom_qty'
            move.amount_total = getattr(order_line, qty_field, False) and (order_line.price_subtotal / getattr(order_line, qty_field) * move.product_uom_qty) or 0


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    amount_total = fields.Float('Monto total', compute='_compute_amount_total')

    @api.depends('move_lines.amount_total')
    def _compute_amount_total(self):
        for pick in self:
            pick.amount_total = sum(pick.move_lines.mapped('amount_total'))

 ```
    
 # Exportar a XLS Excell
 ```
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import xlwt
from datetime import datetime, timedelta, date
import base64
import re
import io


     @api.multi
    def action_download(self):
        for record in self:
            stock_ob = self.env['stock.picking'].search([('esbo_simple_id', '=', record.id)])
            """Limpiamos"""
            if stock_ob:
                for clear in stock_ob:
                    clear.esbo_simple_id = False
            """Agregamos el Stock"""
            row_index = 0

            """Download"""
            workbook = xlwt.Workbook(encoding="utf-8")
            style_title = xlwt.easyxf(
                "font:height 200; font: name Liberation Sans, bold on,color black; align: horiz center")
            currency = xlwt.easyxf('font: height 180; align: wrap yes, horiz right', num_format_str='$#0')
            percent = xlwt.easyxf('font: height 180; align: wrap yes, horiz right', num_format_str='#0%')
            budget_name = "Reporte de Esbo"
            budget_name2 = "Reporte de Esbo"
            today = datetime.today().strftime("%d-%m-%Y")
            worksheet = workbook.add_sheet(budget_name)
            k = 0;
            j = 0
            """cabecera"""
            worksheet.write_merge(k, k, j, j, 'Numero de Albaran', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Codigo Cliente', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Nombre', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Direccion', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Municipio', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'CP', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Pais', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Provincia', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Contacto', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Teléfono', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Codigo Artículo', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Unidades', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'Correo', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'STOCK', style_title);j += 1
            worksheet.write_merge(k, k, j, j, 'EMPRESA', style_title);j += 1
            """línea"""


            for line in record.line_ids:
                line.stock_id.esbo_simple_id = record.id
                record.message_post(body=_("Download: %s") % record.name)
                j = 0
                row_index += 1
                for line_product in line.stock_id.move_lines:
                    worksheet.write(row_index, j, str(line.stock_id.name), );j += 1
                    worksheet.write(row_index, j, "-", );j += 1
                    worksheet.write(row_index, j, str(line.stock_id.sale_info_id.partner_id.name), );j += 1
                    worksheet.write(row_index, j, str(line.stock_id.sale_info_id.partner_id.street), );j += 1
                    worksheet.write(row_index, j, str(line.stock_id.sale_info_id.partner_id.city), );j += 1
                    worksheet.write(row_index, j, str(line.stock_id.sale_info_id.partner_id.zip), );j += 1
                    if line.stock_id.sale_info_id.partner_id.country_id.name:
                        worksheet.write(row_index, j, str(line.stock_id.sale_info_id.partner_id.country_id.name), );j += 1
                    else:
                        worksheet.write(row_index, j, "-", );j += 1

                    if line.stock_id.sale_info_id.partner_id.state_id.name:
                        worksheet.write(row_index, j, str(line.stock_id.sale_info_id.partner_id.state_id.name), );j += 1
                    else:
                        worksheet.write(row_index, j, "-", );j += 1

                    worksheet.write(row_index, j, "-", );j += 1

                    if line.stock_id.sale_info_id.partner_id.mobile:
                        worksheet.write(row_index, j, str(line.stock_id.sale_info_id.partner_id.mobile), );j += 1
                    else:
                        worksheet.write(row_index, j, "-", );j += 1

                    if line_product.product_id.old_sku:
                        worksheet.write(row_index, j, str(line_product.product_id.old_sku), );j += 1
                    else:
                        worksheet.write(row_index, j, "-", );j += 1

                    worksheet.write(row_index, j, str(line_product.product_uom_qty), );j += 1
                    if line.stock_id.sale_info_id.partner_id.email:
                        worksheet.write(row_index, j, str(line.stock_id.sale_info_id.partner_id.email), );j += 1
                    else:
                        worksheet.write(row_index, j, "-", );j += 1

                    worksheet.write(row_index, j, "-", );j += 1
                    company_id = line.stock_id.company_id.id
                    if company_id == 4:
                        worksheet.write(row_index, j, "M", );j += 1
                    elif company_id == 1:
                        worksheet.write(row_index, j, "G", );j += 1
                    else:
                        worksheet.write(row_index, j, "O", );j += 1









            worksheet.col(1).width = 5000
            fp = io.BytesIO()
            workbook.save(fp)
            fp.seek(0)
            data = fp.read()
            fp.close()
            data_b64 = base64.encodestring(data)
            doc = self.env['ir.attachment'].create({
                'name': '%s.xls' % (budget_name2),
                'datas': data_b64,
                'datas_fname': '%s.xls' % (budget_name2),
            })
            return {
                'type': "ir.actions.act_url",
                'url': "web/content/?model=ir.attachment&id=" + str(
                    doc.id) + "&filename_field=datas_fname&field=datas&download=true&filename=" + str(doc.name),
                'target': "self",
                'no_destroy': False,
            }


            record.state = 'done' 
     
      ``` 
  
