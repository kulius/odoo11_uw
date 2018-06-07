# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError
import datetime

class SendStockSaleStock(models.Model):
    _inherit = 'sale.order'

    is_send = fields.Boolean(string='寄倉')
    is_send_out = fields.Boolean(string='寄倉出貨')

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
        return res


class SendStockSaleStockLine(models.Model):
    _inherit = 'sale.order.line'

    send_id = fields.Many2one(comodel_name='send.stock.main', string='寄倉商品')
    show_send_qty = fields.Boolean(compute='compute_boolean', store=True)
    send_id_qty = fields.Float(string='當前寄倉數量')

    @api.depends('order_id.is_send', 'order_id.is_send_out')
    def compute_boolean(self):
        for line in self:
            if line.order_id.is_send is True or line.order_id.is_send_out is True:
                line.show_send_qty = True
            else:
                line.show_send_qty = False

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SendStockSaleStockLine, self).product_id_change()
        send_id = self.env['send.stock.main'].search([('product_id', '=', self.product_id.id), ('partner_id', '=', self.order_partner_id.id)])
        if len(send_id):
            self.send_id = send_id.id
            self.send_id_qty = send_id.last_total
        return res


