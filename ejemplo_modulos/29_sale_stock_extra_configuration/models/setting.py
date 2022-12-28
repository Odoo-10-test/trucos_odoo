
from odoo import models, fields, api, _, tools


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    propose_order_validity = fields.Boolean(string="Propose Order Validity")
    days_ahead = fields.Integer(string="Days Ahead")
    stop_picking_validation = fields.Selection([('yes','Yes'),('no','No')],string="Stop Picking Validation")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        propose_order_validity = params.get_param('propose_order_validity')
        days_ahead = params.get_param('days_ahead')
        stop_picking_validation = params.get_param('stop_picking_validation')
        res.update(
            propose_order_validity=propose_order_validity,
            days_ahead=days_ahead,
            stop_picking_validation=stop_picking_validation
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("propose_order_validity",
                                                         self.propose_order_validity)
        self.env['ir.config_parameter'].sudo().set_param("days_ahead",
                                                         self.days_ahead)
        self.env['ir.config_parameter'].sudo().set_param("stop_picking_validation",
                                                          self.stop_picking_validation)
