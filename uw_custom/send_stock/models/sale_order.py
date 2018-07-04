# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError
import datetime

class SendStockSaleStock(models.Model):
    _inherit = 'sale.order'

    is_send = fields.Boolean(string='寄倉')
    is_send_out = fields.Boolean(string='寄倉出貨')
    order_create_date = fields.Date(string='訂單成立日', default=fields.Date.today)
    order_price_ids = fields.One2many(comodel_name='order.price', inverse_name='order_id')

    driver_id = fields.Many2one(comodel_name='res.users', string='出貨司機')

    @api.onchange('order_line')
    def write_to_price_line(self):
        res = []
        price_res = []
        for line in self.order_line.filtered(lambda r:r.product_uom_qty>0):
            exist = False
            for row in res:
                if row == line.product_id.id:
                    exist = True
            if exist == False:
                res.append(line.product_id.id)
        for line in res:
            price = 0
            sum = 0
            for row in self.order_line.filtered(lambda r:r.product_id.id == line):
                price += row.price_total
                sum += row.product_uom_qty

            price_res.append([0,0,{
                'product_id': line,
                'count': sum,
                'total_price': price,
                'avg_price': price / sum
            }])
        self.update({
            'order_price_ids': price_res
        })


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
                # 沒有send_id_qty了
                # if line.send_id_qty < line.product_uom_qty:
                #     raise UserError("錯誤!! 商品 %s 的寄倉數量不足出貨" % line.product_id.name)
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
        # 不需要確認寄倉單
        # pick = self.picking_ids
        # pick.force_assign()
        # for line in pick.move_lines:
        #     line.write({
        #         'quantity_done': line.product_uom_qty
        #     })
        # pick.button_validate()
        return res


class SendStockSaleStockLine(models.Model):
    _inherit = 'sale.order.line'

    product_wholesale_price = fields.Float(related='product_id.wholesale_price', readonly=True)



class SendStockPriceLine(models.Model):
    _name = 'order.price'

    order_id = fields.Many2one(comodel_name='sale.order')
    product_id = fields.Many2one(comodel_name='product.product', string='產品')
    count = fields.Float(digits=(10, 2),string='數量')
    total_price = fields.Float(digits=(10, 2),string='總價')
    avg_price = fields.Float(digits=(10, 2), string='平均單價')



