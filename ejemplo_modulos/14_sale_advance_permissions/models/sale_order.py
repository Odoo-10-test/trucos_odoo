# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
import os
import tempfile
import csv
from odoo.exceptions import UserError
import base64
import xlrd


class SaleOrder(models.Model):
    _inherit = 'sale.order'

