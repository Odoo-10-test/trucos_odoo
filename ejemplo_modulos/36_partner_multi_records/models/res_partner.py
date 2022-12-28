
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResPartnerPhone(models.Model):
    _name = 'res.partner.phone'
    _description = 'Res Partner Phone'
    _order = "id asc"
    _rec_name = "number"

    partner_id = fields.Many2one('res.partner', string='Cliente', ondelete='cascade', required=True)
    partner_vat = fields.Char('NIF', related='partner_id.vat')
    number = fields.Char(string='Número', required=True)
    notify = fields.Boolean(default=True, string="Notificaciones Activas")

    user_id = fields.Many2one('res.users', string='Usuario', default=lambda self: self.env.user, readonly=1)

    @api.constrains('number')
    def _unique_partner_number(self):
        for phone in self.filtered_domain([('partner_id', '!=', False)]):
            same_numbers = phone.search(
                [('id', '!=', phone.id), ('number', '=', phone.number), ('partner_id', '=', phone.partner_id.id)])
            if same_numbers:
                raise UserError("Se intentó registrar el teléfono %s y ya existe para este contacto" % phone.number)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    phone_ids = fields.One2many('res.partner.phone', 'partner_id')
    phones_count = fields.Integer(compute='_compute_phones', store=True)
    hide_btn_phones = fields.Boolean(compute='_compute_hide_btn_phones')

    def _compute_hide_btn_phones(self):
        for partner in self:
            hide_btn_phones = True
            if self.env.user.has_group('36_partner_multi_records.group_manager_phones'):
                hide_btn_phones = False
            elif self.env.user.has_group('36_partner_multi_records.group_user_phones') and partner.id == self.env.user.partner_id.id:
                    hide_btn_phones = False
            partner.hide_btn_phones = hide_btn_phones

    @api.depends('phone_ids')
    def _compute_phones(self):
        for partner in self:
            partner.phones_count = len(partner.phone_ids)

    def action_view_partner_phones(self):
        action = self.env.ref('36_partner_multi_records.partner_phone_action').sudo().read()[0]
        action['context'] = {'default_partner_id': self.id}
        action['domain'] = [('partner_id', '=', self.id)]
        return action
