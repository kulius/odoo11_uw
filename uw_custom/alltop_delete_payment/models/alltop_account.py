# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AlltopAccount(models.Model):
    _inherit = 'account.invoice'

    got_invoice_name = fields.Char(related='move_name', string='已取得的發票憑證')

    def delete_invoice(self):
        self.got_invoice_name = False
        self.unlink()


class AlltopPayment(models.Model):
    _inherit = 'account.payment'

    got_invoice_name = fields.Char(related='move_name', string='已取得的支付憑證')

    def clean_invoice_name(self):
        self.write({
            'move_name': False
        })
        self.unlink()