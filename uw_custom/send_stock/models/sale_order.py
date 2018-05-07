# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SendStockSaleStock(models.Model):
    _inherit = 'sale.order'

    is_send = fields.Boolean(string='是否寄倉')
