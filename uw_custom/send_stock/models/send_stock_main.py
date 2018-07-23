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

    @api.multi
    def create_sale_out(self):
        partner = []
        for line in self:
            if line.partner_id.id not in partner:
                partner.append(line.partner_id.id)

        if len(partner) == 1:
            res = []
            for row in self:
                res.append([0, 0, {
                    'product_id': row.product_id.id,
                    'name': row.product_id.name,
                    'product_uom': row.product_id.uom_id.id,
                    'price_unit': row.product_id.list_price,
                    'product_uom_qty': row.last_total
                }])

            record = self.env['sale.order'].create({
                'partner_id': self[0].partner_id.id,
                'is_send_out': True,
                'order_line': res
            })

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': record.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'context': {'form_view_initial_mode': 'edit'}
            }
        # 一次產生多筆寄倉出貨單用
        # elif len(partner) > 1:
        #     res = []
        #     records = self.env['sale.order']
        #     for row in out_records:
        #         res.append([0, 0, {
        #             'product_id': row.product_id.id,
        #             'name': row.product_id.name,
        #             'product_uom': row.product_id.uom_id.id,
        #             'price_unit': row.product_id.list_price,
        #             'product_uom_qty': row.last_total
        #         }])
        #
        #     records += self.env['sale.order'].create({
        #         'partner_id': self.partner_out_id.id,
        #         'is_send_out': True,
        #         'order_line': res
        #     })
        #
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'sale.order',
        #         'res_id': records.ids,
        #         'view_type': 'tree,form',
        #         'view_mode': 'tree',
        #         'target': 'current'
        #     }




class SendStockLine(models.Model):
    _name = 'send.stock.line'

    send_id = fields.Many2one(comodel_name='send.stock.main')
    order_id = fields.Many2one(comodel_name='sale.order', string='訂單來源')
    operate_qty = fields.Float(string='數量')
