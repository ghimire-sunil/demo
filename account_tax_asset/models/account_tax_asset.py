# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, Command, fields, models, _
from odoo.exceptions import UserError
import datetime


class FiscalDates(models.Model):
    _inherit = 'account.fiscal.year'
    q1_end = fields.Date(string='1st Q End', store=True)
    q2_start = fields.Date(string='2nd Q Start', store=True)
    q2_end = fields.Date(string='2nd Q End', store=True)
    q3_start = fields.Date(string='3rd QStart', store=True)
    q3_end = fields.Date(string='3rd Q End', store=True)
    q4_start = fields.Date(string='4th Q Start', store=True)


