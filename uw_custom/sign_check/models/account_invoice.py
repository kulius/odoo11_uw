# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError


class AccountInvoiceSignCheck(models.Model):
    _inherit = 'account.invoice'

    sign_check = fields.Boolean(string='簽口收款')
    sign_pay = fields.Boolean(string='簽口付款', compute='compute_sign_pay')

    @api.depends('name')
    def compute_sign_pay(self):
        order = self.env['sale.order'].search([('name','like',self.origin)])
        if len(order):
            self.sign_pay = True

    # def action_invoice_open(self):
    #     res = super(AccountInvoiceSignCheck, self).action_invoice_open()
    #     sign = self.env['sign.main']
    #     if self.sign_check is True:
    #         partner = sign.search([('partner_id', '=', self.partner_id.id)])
    #         if len(partner) > 0:
    #             partner.write({
    #                 'sign_account': [(0, 0, {
    #                     'invoice_from': self.id,
    #                     'price': self.amount_total
    #                 })]
    #             })
    #         else:
    #             sign.create({
    #                 'partner_id': self.partner_id.id,
    #                 'sign_account': [(0, 0, {
    #                     'invoice_from': self.id,
    #                     'price': self.amount_total
    #                 })]
    #             })
    #
    #     if self.sign_pay is True:
    #         partner = sign.search([('partner_id', '=', self.partner_id.id)])
    #         if len(partner) > 0:
    #             less = partner.last_total
    #             if less - self.amount_total < 0:
    #                 raise UserError("錯誤!用戶 %s 剩餘簽口不足付完全額，差額為 %s" % (self.partner_id.name, less))
    #             partner.write({
    #                 'sign_account': [(0, 0, {
    #                     'invoice_from': self.id,
    #                     'price': -self.amount_total
    #                 })]
    #             })
    #         else:
    #             raise UserError("錯誤!用戶 %s 沒有簽口紀錄" % self.partner_id.name)
    #     return res
