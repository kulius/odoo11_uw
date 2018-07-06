# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError
import datetime


# 暫時用不到
# class SendStockProductTemplate(models.Model):
#     _inherit = 'product.template'
#
#     real_unit_price_sale = fields.One2many(comodel_name='order.price', inverse_name='product_tmpl_id')
