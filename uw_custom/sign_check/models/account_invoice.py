# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError


class AccountInvoiceSignCheck(models.Model):
    _inherit = 'account.invoice'

    sign_check = fields.Boolean(string='簽口應收發票')
    sign_pay = fields.Boolean(string='待定義。')
    sign_main_id = fields.Many2one(comodel_name='sign.main')



class AccountPaymentSignCheck(models.Model):
    _inherit = 'account.payment'

    @api.onchange('journal_id')
    def set_default_iournal_id(self):
        if self.invoice_ids:
            for line in self.invoice_ids:
                if line.sign_pay is True:
                    sign_book = self.env['account.journal'].search([('name', 'like', '簽口')])
                    self.journal_id = sign_book.id
                    return {'domain': {'journal_id': [('name', 'like', '簽口')]}}
