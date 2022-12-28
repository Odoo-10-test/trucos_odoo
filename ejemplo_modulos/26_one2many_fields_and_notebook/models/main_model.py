#-*- coding: utf-8 -*-

from odoo import fields, models, api, _


class MainModel(models.Model):
    _name = "main.model"
    _description = "Main Model"
    _order = 'id desc'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    name = fields.Char(string='Name', default=_("New"))
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    notes = fields.Text(string='Notes')
    line_ids = fields.One2many('main.model.line', 'main_model_id', string='Lines')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('main.model') or _('New')
        return super().create(vals)


class MainModelLine(models.Model):
    _name = "main.model.line"
    _description = "Main Model Line"

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)
    main_model_id = fields.Many2one('main.model', string='Main Model')





