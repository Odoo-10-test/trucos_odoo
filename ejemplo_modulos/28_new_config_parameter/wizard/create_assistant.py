#-*- coding: utf-8 -*-

import os
import csv
import tempfile
from odoo.exceptions import UserError
from odoo import fields, models, api, _
import base64
from datetime import datetime, date
import xlrd


class CreateAssistant(models.TransientModel):
    _name = "create.assistant"
    _description = "Create Assistant"

    name = fields.Char(string="Name", required=True)
    record_type = fields.Selection([('product.template','Product'),('res.partner','Contact')],string="Record Type", readonly=1)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        params = self.env['ir.config_parameter'].sudo()
        record_type = params.get_param('record_type')
        res['record_type'] = record_type
        return res

    def action_create_record(self):
        if not self.record_type:
            raise UserError(_('Please set record type in module configuration.'))
        record = self.env[self.record_type].create({'name':self.name})
        name = dict(self._fields['record_type'].selection).get(self.record_type)
        return {
            'name': name,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self.record_type,
            'res_id': record.id,
            'type': 'ir.actions.act_window',
        }




