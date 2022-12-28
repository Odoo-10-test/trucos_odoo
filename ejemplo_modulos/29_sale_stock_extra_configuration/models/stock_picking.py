# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        params = self.env['ir.config_parameter'].sudo()
        stop_picking_validation = params.get_param('stop_picking_validation')
        if stop_picking_validation == 'yes':
            raise UserError(_('The current picking validation is stopped.'))
        return super(StockPicking, self).button_validate()



 
