# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError
import datetime

class SendStockSaleStock(models.Model):
    _inherit = 'sale.order'

    is_send = fields.Boolean(string='寄倉')
    is_send_out = fields.Boolean(string='寄倉出貨')
    order_create_date = fields.Date(string='訂單成立日', default=fields.Date.today)
    order_price_ids = fields.One2many(comodel_name='order.price', inverse_name='order_id', compute='write_to_price_line',store=True)

    driver_id = fields.Many2one(comodel_name='res.users', string='出貨司機')

    @api.depends('order_line')
    def write_to_price_line(self):

        for line in self:
            res = []
            price_res = []
            for row in line.order_line.filtered(lambda r: r.product_uom_qty > 0):
                exist = False
                for obj in res:
                    if obj == row.product_id.id:
                        exist = True
                if exist == False:
                    res.append(row.product_id.id)

            for row in res:
                price = 0
                sum = 0
                for obj in self.order_line.filtered(lambda r:r.product_id.id == row):
                    price += obj.price_total
                    sum += obj.product_uom_qty

                price_res.append([0,0,{
                    'product_id': row,
                    'count': sum,
                    'total_price': price,
                    'avg_price': price / sum
                }])
                line.order_price_ids = price_res

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

            self.picking_ids.unlink()
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
        return res


class SendStockSaleStockLine(models.Model):
    _inherit = 'sale.order.line'

    product_wholesale_price = fields.Float(related='product_id.wholesale_price', readonly=True, string='產品定價')
    real_price_unit = fields.Float(digits=(10, 2), compute='compute_real_price_unit',store=True, string='平均單價')

    # 同時計算明細同商品的平均單價，但只能取得最新價格放到當前紀錄(one2many內)，未存檔前商品平均價格可能未會不一致，但存檔後相同商品單價會一致
    @api.depends('product_uom_qty', 'price_unit')
    def compute_real_price_unit(self):
        for row in self:
            order_line = row.order_id.order_line
            sum = 0
            price = 0
            for line in order_line.filtered(lambda r: r.product_id.id == row.product_id.id):
                sum += line.product_uom_qty
                price += line.price_total
            for line in order_line.filtered(lambda r: r.product_id.id == row.product_id.id):
                if sum != 0:
                    line.real_price_unit = price / sum
                else:
                    line.real_price_unit = 0


class SendStockPriceLine(models.Model):
    _name = 'order.price'

    order_id = fields.Many2one(comodel_name='sale.order')
    product_id = fields.Many2one(comodel_name='product.product', string='產品')
    # 暫時用不到
    # product_tmpl_id = fields.Many2one(comodel_name='product.template', related='product_id.product_tmpl_id', store=True, string='產品範本')
    count = fields.Float(digits=(10, 2), string='數量')
    total_price = fields.Float(digits=(10, 2),string='總價')
    avg_price = fields.Float(digits=(10, 2), string='平均單價')



