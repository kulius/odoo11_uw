# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError
import datetime


class SignCheckSaleOrder(models.Model):
    _inherit = 'sale.order'

    mutex_sign = fields.Boolean(string='互斥', compute='mutex_set')
    is_sign = fields.Boolean(string='簽口')
    is_sign_pay = fields.Boolean(string='簽口出貨')
    partner_sign_total = fields.Float(string='客戶簽口金額', compute='compute_sign_used')
    partner_cost_toal = fields.Float(string='花費金額', compute='compute_sign_used')
    partner_less_price = fields.Float(string='剩餘簽口金額', compute='compute_sign_used')

    @api.depends('is_send', 'is_send_out', 'is_sign_pay', 'is_sign')
    def mutex_set(self):
        for line in self:
            if line.is_send is True:
                line.mutex_sign = True
            elif line.is_send_out is True:
                line.mutex_sign = True
            elif line.is_sign_pay is True:
                line.mutex_sign = True
            elif line.is_sign is True:
                line.mutex_sign = True
            elif line.is_send is False:
                line.mutex_sign = False
            elif line.is_send_out is False:
                line.mutex_sign = False
            elif line.is_sign_pay is False:
                line.mutex_sign = False
            elif line.is_sign is False:
                line.mutex_sign = False


    @api.depends('order_line', 'partner_id')
    def compute_sign_used(self):
        for line in self:
            partner = self.env['sign.main'].search([('partner_id', '=', self.partner_id.id)])
            amount_untaxed = amount_tax = 0.0
            for row in line.order_line:
                amount_untaxed += row.price_subtotal
                amount_tax += row.price_tax
            amount_total = amount_untaxed+amount_tax

            if len(partner) > 0:
                line.partner_sign_total = partner.last_total
                line.partner_cost_toal = amount_total
                line.partner_less_price = partner.last_total - amount_total

class SaleOrderLineSignCheck(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def filter_product(self):
        if self.order_id.is_sign or self.order_id.is_sign_pay:
            return {
                'domain': {
                    'product_id': [('is_sign_product', '=', True)],
                }}
