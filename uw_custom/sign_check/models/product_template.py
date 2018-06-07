# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError


class SignCheckProductTemplate(models.Model):
    _inherit = 'product.template'

    is_sign_product = fields.Boolean(string='簽口產品')
