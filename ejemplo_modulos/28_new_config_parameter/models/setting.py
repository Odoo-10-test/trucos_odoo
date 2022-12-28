
from odoo import models, fields, api, _, tools


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    record_type = fields.Selection([('product.template','Product'),('res.partner','Contact')],string="Record Type",default='product.template')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        record_type = params.get_param('record_type')
        res.update(
            record_type=record_type,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("record_type", self.record_type)
