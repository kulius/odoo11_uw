# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SignMain(models.Model):
    _name = 'sign.main'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one(comodel_name='res.partner', string='客戶')
    last_total = fields.Integer(string='剩餘簽口金額', compute='compute_total', store=True)
    order_total = fields.Integer(string='報價(銷售)單總金額', compute='compute_order_total')
    invoice_total = fields.Integer(string='簽口未付帳單金額', compute='compute_invoice_total')
    sign_account = fields.One2many(comodel_name='sign.main.line', inverse_name='sign_id', string='變動明細')
    order_ids = fields.One2many(comodel_name='sale.order', inverse_name='sign_main_id',
                                domain=[('invoice_status', 'in', ['no', 'to invoice'])], string='報價(銷售)報價單')
    invoice_ids = fields.One2many(comodel_name='account.invoice', inverse_name='sign_main_id',
                                  domain=[('state', 'in', ['draft', 'open'])], string='簽口未付帳單')
    group_custom_id = fields.Many2one(related='partner_id.group_custom_id', store=True)
    # group_ids = fields.One2many(comodel_name='sign.main.group', inverse_name='sign_id', compute='compute_group', store=True, string='客戶群組')


    @api.multi
    def name_get(self):
        res = []
        for order in self:
            name = '%s - 簽口 %d' % (order.partner_id.name, order.last_total)
            res.append((order.id, name))
        return res

    @api.depends('group_custom_id.group_ids')
    def compute_group(self):
        for line in self:
            res = []
            for row in line.group_custom_id.group_ids:
                if len(row.sign_ids) == 1:
                    res.append([0, 0, {
                        'group_id': row.sign_ids[0].id
                    }])

            line.update({
                'group_ids': res
            })



    @api.depends('invoice_ids')
    def compute_invoice_total(self):
        for line in self:
            sum = 0
            for invoice in line.invoice_ids.filtered(lambda r: r.state in ['draft', 'open']):
                sum += invoice.amount_total_signed
            line.invoice_total = sum



    @api.depends('order_ids')
    def compute_order_total(self):
        for line in self:
            sum = 0
            for order in line.order_ids.filtered(lambda r: r.invoice_status in ['no','to invoice']):
                sum += order.amount_total
            line.order_total = sum

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
    sign_invoice = fields.Many2one(comodel_name='account.invoice', string='來源帳單')
    price = fields.Integer(string='金額')


class SignMainGroup(models.Model):
    _name = 'sign.main.group'

    sign_id = fields.Many2one(comodel_name='sign.main')
    group_id = fields.Many2one(comodel_name='sign.main')
    price = fields.Integer(related='group_id.last_total')


