# _*_ coding: utf-8 _*_
from odoo import models, api,fields
import datetime

class SendStockSaleStock(models.Model):
    _inherit = 'sale.order'

    is_send = fields.Boolean(string='是否寄倉')
    is_send_out = fields.Boolean(string='是否寄倉出貨')

    @api.multi
    def action_confirm(self):
        res = super(SendStockSaleStock, self).action_confirm()
        if self.is_send is True:
            send = self.env['send.stock.line']
            for line in self.order_line:
                send.create({
                    'send_date': datetime.datetime.now(),
                    'order_id': self.id,
                    'partner_id': self.partner_id.id,
                    'origin_qty': line.product_uom_qty,
                    'product_id': line.product_id.id
                })
        return res



class SendStockSaleStockLine(models.Model):
    _inherit = 'sale.order.line'

    send_id = fields.Many2one(comodel_name='send.stock.line', string='寄倉商品')
    send_id_qty = fields.Float(string='寄倉可出數量')

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SendStockSaleStockLine, self).product_id_change()
        send_id = self.env['send.stock.line'].search([('product_id', '=', self.product_id.id), ('partner_id', '=', self.order_id.partner_id.id)])
        print(send_id)
        self.send_id = send_id
        self.send_id_qty = send_id.remain_qty
        return res


