# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SendStockMain(models.Model):
    _name = 'send.stock.main'

    partner_id = fields.Many2one(comodel_name='res.partner', string='客戶')
    product_id = fields.Many2one(comodel_name='product.product', string='產品')
    last_total = fields.Float(string='剩餘數量', compute='compute_total', store=True)
    send_ids = fields.One2many(comodel_name='send.stock.line', inverse_name='send_id', string='寄倉明細')

    @api.depends('send_ids')
    def compute_total(self):
        for line in self:
            sum = 0.0
            for row in line.send_ids:
                sum = sum + row.operate_qty

            line.last_total = sum


class SendStockLine(models.Model):
    _name = 'send.stock.line'

    send_id = fields.Many2one(comodel_name='send.stock.main')
    order_id = fields.Many2one(comodel_name='sale.order', string='訂單來源')
    operate_qty = fields.Float(string='數量')
