# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SignInvoice(models.Model):
    _name = 'sign.invoice'

    name = fields.Char(string='名稱')
    partner_id = fields.Many2one(comodel_name='res.partner', string='客戶名稱')
    partner_sign_price = fields.Float(string='當時剩餘簽口')
    check_invoice_ids = fields.Many2many(comodel_name='account.invoice', string='勾選的發票')
    check_invoice_total = fields.Float(string='簽口發票金額', compute='compute_total_price')
    sign_invoice_line_ids = fields.One2many(comodel_name='sign.invoice.line', inverse_name='sign_id', string='簽口明細')
    sign_invoice_ids_total = fields.Float(string='購買簽口價值', compute='compute_total_price')
    sign_invoice_pay = fields.Float(string='實際購買簽口金額', compute='compute_total_price')
    less_sign_price = fields.Float(string='剩餘簽口金額', compute='compute_total_price')
    created_invoice = fields.Many2one(comodel_name='account.invoice', string='建立的發票', readonly=True)
    state = fields.Selection(selection=[('draft', '草稿'), ('invoiced', '已開發票')], default='draft')
    batch_id = fields.Many2one(comodel_name='sign.batch')

    def write_sign_line(self, invoice, sign):
        # sign代表是否為 買簽口(增加) 或 簽口付款 (減少)
        partner = self.env['sign.main'].search([('partner_id', '=', self.partner_id.id)])
        if len(partner) > 0:
            if sign:
                partner.write({
                    'sign_account': [(0, 0, {
                        'sign_invoice': invoice.id,
                        'price': self.sign_invoice_ids_total
                    })]
                })
            else:
                partner.write({
                    'sign_account': [(0, 0, {
                        'sign_invoice': invoice.id,
                        'price': -invoice.amount_total
                    })]
                })


    def create_invoice(self):
        invoice_lines = []
        for line in self.sign_invoice_line_ids:
            invoice_lines.append([0, 0, {
                'product_id': line.product_id.id,
                'uom_id': line.product_id.uom_id.id,
                'quantity': 1.0,
                'price_unit': line.price,
                'name': line.product_id.name,
                'account_id': line.product_id.property_account_income_id.id or line.product_id.categ_id.property_account_income_categ_id.id,
            }])
        res = self.env['account.invoice'].create({
            'account_id': self.partner_id.property_account_receivable_id.id,
            'partner_id': self.partner_id.id,
            'invoice_line_ids': invoice_lines,
            'sign_pay': 1,
            'name': '簽口發票' + str(self.id),
            'type': 'out_invoice',
        })
        self.created_invoice = res.id
        self.name = '簽口' + str(self.id)
        self.write_sign_line(res, True)

    def open_and_pay_invoice(self):
        # 一次做完買簽口發票的打開與登記付款
        self.create_invoice()
        self.created_invoice.action_invoice_open()
        journal = self.env['account.journal'].search([('name', 'like', '簽口')], limit=1)
        self.created_invoice.pay_and_reconcile(journal, self.created_invoice.amount_total)
        self.state = 'invoiced'

        # 將簽口未付發票變成打開狀態
        for line in self.check_invoice_ids:
            line.action_invoice_open()
            line.pay_and_reconcile(journal, line.amount_total)
            self.write_sign_line(line, False)

    @api.onchange('partner_id')
    def comput_set(self):
        partner = self.env['sign.main'].search([('partner_id', '=', self.partner_id.id)])
        if len(partner) > 0:
            self.partner_sign_price = partner.last_total
        invoice_ids = self.env['account.invoice'].search([('partner_id', '=', self.partner_id.id),('state', '=', 'draft'), ('sign_check', '=', True)])
        data =[]
        for line in invoice_ids:
            data.append([4, line.id])

        self.check_invoice_ids = data
        return {'domain':
                    {'check_invoice_ids':
                         [('partner_id', '=', self.partner_id.id), ('state', '=', 'draft'), ('sign_check', '=', True)]
                     }
                }
    @api.depends('check_invoice_ids', 'sign_invoice_line_ids')
    def compute_total_price(self):
        for line in self:
            check_sum = 0.0
            sign_sum = 0.0
            pay_sum = 0.0
            for row in line.check_invoice_ids:
                check_sum += row.amount_total
            for sign_row in line.sign_invoice_line_ids:
                sign_sum += sign_row.sign_price
                pay_sum +=sign_row.price

            line.check_invoice_total = check_sum
            line.sign_invoice_ids_total = sign_sum
            line.less_sign_price = line.partner_sign_price - check_sum + sign_sum
            line.sign_invoice_pay = pay_sum


class SignInvoiceLine(models.Model):
    _name = 'sign.invoice.line'

    sign_id = fields.Many2one(comodel_name='sign.invoice')
    product_id = fields.Many2one(comodel_name='product.product', string='簽口產品', domain=[('name', 'like', '簽口')])
    price = fields.Float(string='支付金額')
    sign_price = fields.Float(string='簽口價值', compute='cmpute_sign_price')
    sign_discount = fields.Float(string='簽口優惠', compute='cmpute_sign_price')
    cash_discount = fields.Float(string='現金優惠')
    is_paid = fields.Boolean(string='已收款')

    def pay_the_paid(self):
        self.is_paid = True

    @api.onchange('product_id')
    def onchang_product_id(self):
        res = self.env['product.product'].search([('name', 'like', '簽口')])
        if len(res) == 1:
            self.product_id = res.id

    @api.depends('price')
    def cmpute_sign_price(self):
        # 可能需要將price跟cash_discount分開處理
        # key 錯先金優惠金額 1500 > 3000 支付金額卻是 48500 > 45500 應該是 47000
        for line in self:
            total = line.price + line.cash_discount
            times1 = 0.0
            times2 = 0.0
            while total >= 30000:
                if total >= 50000:
                    total = total - 50000
                    times1 += 1
                elif total >= 30000:
                    total = total - 30000
                    times2 += 1
            line.sign_price = line.price + 10000*times1 + 3000*times2 + line.cash_discount
            line.sign_discount = 10000*times1 + 3000*times2 + line.cash_discount

    @api.onchange('cash_discount')
    def set_price(self):
        self.price = self.price - self.cash_discount


class SignBatch(models.Model):
    _name = 'sign.batch'

    date_from = fields.Date(string='開始時間')
    date_to = fields.Date(string='結束時間')
    name = fields.Char(string='名稱')
    sign_main_ids = fields.One2many(comodel_name='sign.batch.line', inverse_name='batch_id')



    @api.onchange('date_to')
    def set_sign_invoice(self):
        if self.date_to is False:
            return
        partner = self.env['res.partner']
        invoice = self.env['account.invoice'].search([('state', '=', 'draft'),('sign_check', '=', True)])
        for line in invoice:
            exist = False
            for row in partner:
                if row.id == line.partner_id.id:
                    exist = True

            if exist == False and self.date_to != False:
                partner += line.partner_id

        product = self.env['product.product'].search([('name','like', '簽口')], limit=1)

        res =[]
        for line in partner:
            invoice_ids = self.env['account.invoice']
            sum = 0
            compute_sign = 30000
            for row in invoice.filtered(lambda r:r.partner_id.id == line.id):
                invoice_ids += row
                sum += row.amount_total

            if sum > 30000:
                compute_sign = 50000

            res.append([0, 0, {
                'partner_id': line.id,
                'invoice_amount': sum,
                'sign_amount': compute_sign
            }])
        self.sign_main_ids = res


class SignBatchLine(models.Model):
    _name = 'sign.batch.line'

    batch_id = fields.Many2one(comodel_name='sign.batch')
    partner_id = fields.Many2one(comodel_name='res.partner', string='客戶名稱')
    invoice_amount = fields.Float(string='發票總金額')
    sign_amount = fields.Float(string='簽口金額')
    invoice_ids = fields.Char()


    # @api.depends('invoice_ids')
    # def compute_invoice_amount(self):
    #     for line in self:
    #         res = self.env['account.invoice'].search([('id', 'in', line.invoice_ids)])
    #         sum = 0.0
    #         for row in line:
    #             sum += row.amount_total
    #
    #         line.invoice_amount = sum












