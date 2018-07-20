# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.tools.translate import _
from odoo.exceptions import UserError


class StockOut(models.TransientModel):
    _name = 'stock.out'

    partner_id = fields.Many2one(comodel_name='res.partner', string='寄倉客戶名稱')
    related_partner_id = fields.Many2one(related='partner_id', readonly=True)
    partner_out_id = fields.Many2one(comodel_name='res.partner', string='出貨客戶名稱')
    related_pratner_group_id = fields.Many2one(related='partner_id.group_custom_id')
    out_ids = fields.One2many(comodel_name='stock.out.line', inverse_name='out_id')

    @api.onchange('partner_id')
    def set_default(self):
        if self.env.context.get('active_model', '') == 'send.stock.main':
            ids = self.env.context['active_ids']
            stock = self.env['send.stock.main'].browse(ids)
            res = []
            for line in stock:
                res.append([0, 0, {
                    'send_stock_id': line.id,
                }])

            self.update({
                'partner_id': stock[0].partner_id.id,
                'partner_out_id': stock[0].partner_id.id,
                'out_ids': res
                })

            if self.partner_id.group_custom_id:
                group = self.partner_id.group_custom_id.id
                return {'domain': {
                    'partner_out_id': [('group_custom_id', '=', group)]
                }}
            else:
                return {'domain': {
                    'partner_out_id': [('id', '=', self.partner_id.id)]
                }}




    def create_stock_out(self):
        sale = self.env['sale.order']
        res = []
        for line in self.out_ids.filtered(lambda r: r.out_qty > 0):
            print(line.product_id)
            res.append([0, 0, {
                'product_id': line.change_product_id.id,
                'name': line.change_product_id.name,
                'product_uom': line.change_product_id.uom_id.id,
                'price_unit': line.change_product_id.list_price,
                'product_uom_qty': line.out_qty
            }])
        record = sale.create({
            'partner_id': self.partner_out_id.id,
            'is_send_out': True,
            'order_line': res
        })
        action = self.env.ref('send_stock.send_stock_order_action3').read()[0]
        action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
        action['res_id'] = record.id
        return action


class StockOutLine(models.TransientModel):
    _name = 'stock.out.line'

    out_id = fields.Many2one(comodel_name='stock.out')
    send_stock_id = fields.Many2one(comodel_name='send.stock.main')
    product_id = fields.Many2one(related='send_stock_id.product_id', store=True, readonly=True)
    related_product_group_id = fields.Many2one(related='product_id.group_product_id', store=True)
    change_product_id = fields.Many2one(comodel_name='product.product', string='出貨產品')
    last_total = fields.Float(related='send_stock_id.last_total')
    out_qty = fields.Float(string='要出貨的數量')

    @api.onchange('out_qty')
    def check_qty(self):
        if self.out_qty > self.last_total:
            raise UserError(_(u'出貨數量大於寄倉數量！'))

    @api.onchange('change_product_id')
    def domain_change_product(self):
        print('123')
        if self.change_product_id:
            if self.product_id.group_product_id:
                group = self.product_id.group_product_id.id
                return {'domain': {
                    'change_product_id': [('group_product_id', '=', group)]
                }}
            else:
                return {'domain': {
                    'change_product_id': [('id', '=', self.product_id.id)]
                }}

        else:
            return {'domain': {
                'change_product_id': [('id', '=', self.product_id.id)]
            }}