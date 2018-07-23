# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError


class SignCheckResPartner(models.Model):
    _inherit = 'res.partner'

    is_month_account = fields.Boolean(string='月結用戶')
    sign_ids = fields.One2many(comodel_name='sign.main', inverse_name='partner_id')
