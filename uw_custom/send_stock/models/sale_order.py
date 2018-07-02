# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError
import datetime

class SendStockSaleStock(models.Model):
    _inherit = 'sale.order'

    is_send = fields.Boolean(string='寄倉')
    is_send_out = fields.Boolean(string='寄倉出貨')
    order_create_date = fields.Date(string='訂單成立日', default=fields.Date.today)
    avg_price = fields.Float(digits=(10, 2), compute='compute_avg_price', string='平均單價')

    def compute_avg_price(self):
        for line in self:
            price_sum = 0
            qty_sum = 0
            for row in line.order_line:
                price_sum += row.price_unit * row.product_uom_qty
                qty_sum += row.product_uom_qty

            if qty_sum != 0:
                line.avg_price = price_sum/qty_sum

    @api.multi
    def action_confirm(self):
        res = super(SendStockSaleStock, self).action_confirm()
        send = self.env['send.stock.main']
        if self.is_send is True:
            for line in self.order_line:
                product = send.search([('partner_id', '=', self.partner_id.id), ('product_id', '=', line.product_id.id)])

                if len(product) > 0:
                    product.write({
                        'send_ids': [(0, 0, {
                            'order_id': self.id,
                            'operate_qty': line.product_uom_qty
                        })]
                    })
                else:
                    send.create({
                        'partner_id': self.partner_id.id,
                        'product_id': line.product_id.id,
                        'send_ids': [(0, 0, {
                            'order_id': self.id,
                            'operate_qty': line.product_uom_qty
                        })]
                    })
        if self.is_send_out is True:
            for line in self.order_line:
                if line.send_id_qty < line.product_uom_qty:
                    raise UserError("錯誤!! 商品 %s 的寄倉數量不足出貨" % line.product_id.name)
                product = send.search(
                    [('partner_id', '=', self.partner_id.id), ('product_id', '=', line.product_id.id)])

                if len(product) > 0:
                    product.write({
                        'send_ids': [(0, 0, {
                            'order_id': self.id,
                            'operate_qty': -line.product_uom_qty
                        })]
                    })
                else:
                    raise UserError("錯誤!! 商品 %s 沒有寄倉庫存" % line.product_id.name)

        pick = self.picking_ids
        pick.force_assign()
        for line in pick.move_lines:
            line.write({
                'quantity_done': line.product_uom_qty
            })
        pick.button_validate()
        return res


class SendStockSaleStockLine(models.Model):
    _inherit = 'sale.order.line'

    product_wholesale_price = fields.Float(related='product_id.wholesale_price', readonly=True)



