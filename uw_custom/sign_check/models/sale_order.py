# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError
import datetime


class SignCheckSaleOrder(models.Model):
    _inherit = 'sale.order'

    mutex_sign = fields.Boolean(string='互斥')
    is_sign = fields.Boolean(string='簽口')
    is_sign_pay = fields.Boolean(string='簽口出貨')
    partner_sign_total = fields.Float(string='客戶簽口金額', compute='compute_sign_used')
    partner_cost_toal = fields.Float(string='花費金額', compute='compute_sign_used')
    partner_less_price = fields.Float(string='剩餘簽口金額', compute='compute_sign_used')

    @api.onchange('is_send', 'is_send_out', 'is_sign_pay', 'is_sign')
    def mutex_set(self):
        if self.is_send is True:
            self.mutex_sign = True
        elif self.is_send_out is True:
            self.mutex_sign = True
        elif self.is_sign_pay is True:
            self.mutex_sign = True
        elif self.is_sign is True:
            self.mutex_sign = True
        elif self.is_send is False:
            self.mutex_sign = False
        elif self.is_send_out is False:
            self.mutex_sign = False
        elif self.is_sign_pay is False:
            self.mutex_sign = False
        elif self.is_sign is False:
            self.mutex_sign = False


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


    @api.multi
    def action_confirm(self):
        res = super(SignCheckSaleOrder, self).action_confirm()
        sign = self.env['sign.main']
        if self.is_sign is True:
            partner = sign.search([('partner_id', '=', self.partner_id.id)])
            if len(partner) > 0:
                partner.write({
                    'sign_account': [(0, 0, {
                        'sale_from': self.id,
                        'price': self.amount_total
                    })]
                })
            else:
                sign.create({
                    'partner_id': self.partner_id.id,
                    'sign_account': [(0, 0, {
                        'sale_from': self.id,
                        'price': self.amount_total
                    })]
                })

        if self.is_sign_pay is True:
            partner = sign.search([('partner_id', '=', self.partner_id.id)])
            if len(partner) > 0:
                less = partner.last_total - self.amount_total

                if less < 0:
                    raise UserError("錯誤!用戶 %s 剩餘簽口不足付完全額，差額為 %s" % (self.partner_id.name, less))
                partner.write({
                    'sign_account': [(0, 0, {
                        'sale_from': self.id,
                        'price': -self.amount_total
                    })]
                })
            else:
                raise UserError("錯誤!用戶 %s 沒有簽口紀錄" % self.partner_id.name)
        return res


class SaleOrderLineSignCheck(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def filter_product(self):
        if self.order_id.is_sign:
            return {
                'domain': {
                    'product_id': [('name', 'like', '簽口')],
                }}
