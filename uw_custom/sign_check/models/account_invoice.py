# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError


class AccountInvoiceSignCheck(models.Model):
    _inherit = 'account.invoice'

    sign_check = fields.Boolean(string='簽口應收發票')
    sign_pay = fields.Boolean(string='買簽口')
    sign_main_id = fields.Many2one(comodel_name='sign.main')



class AccountPaymentSignCheck(models.Model):
    _inherit = 'account.payment'

    def action_validate_invoice_payment(self):
        res = super(AccountPaymentSignCheck,self).action_validate_invoice_payment()
        sign_book = self.env['account.journal'].search([('name', 'like', '簽口')])
        if self.invoice_ids and self.journal_id == sign_book:
            for line in self.invoice_ids:
                partner = self.env['sign.main'].search([('partner_id', '=', line.partner_id.id)])
                # 簽口應收付款需要扣錢
                if len(partner) == 1 and line.sign_check is True:
                    partner.write({
                        'sign_account': [(0, 0, {
                            'sign_invoice': line.id,
                            'price': -self.amount
                        })]
                    })
                # 買簽口付款需要加錢
                elif len(partner) == 1 and line.sign_pay is True:
                    partner.write({
                        'sign_account': [(0, 0, {
                            'sign_invoice': line.id,
                            'price': self.amount
                        })]
                    })
        return res

    @api.onchange('journal_id')
    def set_default_iournal_id(self):
        if self.invoice_ids:
            for line in self.invoice_ids:
                if line.sign_pay is True or line.sign_check is True:
                    sign_book = self.env['account.journal'].search([('name', 'like', '簽口')])
                    self.journal_id = sign_book.id
                    return {'domain': {'journal_id': [('name', 'like', '簽口')]}}
