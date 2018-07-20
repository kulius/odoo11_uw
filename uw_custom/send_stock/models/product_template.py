# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError
import datetime


class SendStockProductTemplate(models.Model):
    _inherit = 'product.template'

    group_product_id = fields.Many2one(comodel_name='group.product', string='群組')

