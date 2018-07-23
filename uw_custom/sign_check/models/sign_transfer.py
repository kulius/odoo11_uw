# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError


class SignTransfer(models.Model):
    _name = 'sign.transfer'

    name = fields.Char()
    partner_out_id = fields.Many2one(comodel_name='sign.main', string='轉出客戶')
    partner_out_price = fields.Integer(related='partner_out_id.last_total', string='轉出客戶簽口餘額')
    partner_in_price = fields.Integer(related='partner_in_id.last_total', string='專入客戶簽口餘額')
    transfer_price = fields.Integer(string='轉入金額')
    # partner_group_ids = fields.One2many()
    partner_in_id = fields.Many2one(comodel_name='sign.main', string='轉入客戶')
    state = fields.Selection(selection=[('draft', '草稿'), ('invoiced', '已轉出')])

    @api.onchange('partner_out_id')
    def domain_partner_in(self):
        partner = self.env['sign.main'].search([('last_total', '>', 0)])

        if self.partner_out_id:
            if self.partner_out_id.group_custom_id:
                group = self.partner_out_id.group_custom_id.id
                return {'domain': {
                    'partner_in_id': [('group_custom_id', '=', group)]
                }}
            else:
                raise UserError(u'該轉出客戶沒有設定群組!!無法使用本功能')
        else:
            return {'domain': {
                    'partner_out_id': [('id', '=', partner.ids)]
                }}

    @api.onchange('transfer_price')
    def check_transfer_price(self):
        if self.transfer_price > self.partner_out_price:
            raise UserError(u'超過轉出上限!轉出客戶簽口餘額不足')
        elif self.transfer_price < 0:
            raise UserError(u'轉出金額必須大於0')
