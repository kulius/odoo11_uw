# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SignMain(models.Model):
    _name = 'sign.main'

    partner_id = fields.Many2one(comodel_name='res.partner', string='客戶')
    last_total = fields.Integer(string='剩餘金額', compute='compute_total')
    sign_account = fields.One2many(comodel_name='sign.main.line', inverse_name='sign_id', string='變動明細')

    @api.depends('sign_account')
    def compute_total(self):
        for line in self:
            sum = 0
            for row in line.sign_account:
                sum = sum + row.price

            line.last_total = sum


class SignMainLine(models.Model):
    _name = 'sign.main.line'

    sign_id = fields.Many2one(comodel_name='sign.main')
    sale_from = fields.Many2one(comodel_name='sale.order', string='來源訂單')
    sign_from = fields.Many2one(comodel_name='sign.invoice', string='來源簽口結帳')
    price = fields.Integer(string='金額')

