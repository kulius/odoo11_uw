# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SendStockLine(models.Model):
    _name = 'send.stock.line'

    name = fields.Char(related='product_id.name')
    send_date = fields.Date(string='寄倉時間')
    order_id = fields.Many2one(comodel_name='sale.order', string='訂單來源')
    partner_id = fields.Many2one(comodel_name='res.partner', string='客戶')
    product_id = fields.Many2one(comodel_name='product.product', string='產品')
    origin_qty = fields.Float(string='初始數量')
    used_qty = fields.Float(string='出貨數量', compute='compute_send_qty', store=True)
    remain_qty = fields.Float(string='剩餘數量', compute='compute_send_qty', store=True)
    order_line_ids = fields.One2many(comodel_name='sale.order.line', inverse_name='send_id')

    @api.depends('order_line_ids')
    def compute_send_qty(self):
        for line in self:
            sum = 0
            for row in line.order_line_ids:
                a = row.product_uom_qty
                sum += a

            line.used_qty = sum
            line.remain_qty = line.origin_qty - sum