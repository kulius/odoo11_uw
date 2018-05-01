# -*- coding: utf-8 -*-
from odoo import models,fields,api

class Accountinvoicepaper(models.Model):
    _name = "account.invoice.paper"

    invoice_paper = fields.Char(string=u"紙本發票號碼")
    invoice_paper_date = fields.Date(string=u"紙本發票日期")
    partner_id = fields.Many2one(comodel_name = 'res.partner', string='客戶')
    invoice_ids = fields.One2many(comodel_name='account.invoice.paper.line',inverse_name='invoice_paper_id',string='紙本發票明細')

    @api.model
    def create(self, values):
        res_id = super(Accountinvoicepaper, self).create(values)
        res = self.env['sale.order']


        for line in res_id.invoice_ids:
            res += line

        for line in res:
            line.action_invoice_create(final=True)

        res_id.invoice_paper = self.env['ir.sequence'].next_by_code('account.invoice.paper')

        return res_id



class invoicefrommultisaleorder(models.Model):
    _inherit = "account.invoice"

    sale_order_id = fields.Many2one(comodel_name='sale.order', string='銷售訂單', domain=[('invoice_status', '=', 'to invoice')])

    @api.model
    def create(self, vals):
        res_id = super(invoicefrommultisaleorder, self).create(vals)
        r = []
        res = self.env['sale.order']
        for line in res_id.invoice_line_ids:
            if line.origin not in r and res_id.origin:
                res_id.origin += ' ' + line.origin
                r.append(line.origin)

            elif not res_id.origin:
                res_id.origin = line.origin
                r.append(line.origin)

        for line in r:
            res = self.env['sale.order'].search([('name', '=', line)])
            for row in res:
                row.invoice_status = 'invoiced'
            # invoices = res.action_invoice_create(final=True)

        return res_id

    @api.multi
    def unlink(self):
        for line in self:
            for row in line.invoice_line_ids:
                res = self.env['sale.order'].search([('name', '=', row.origin)])
                if res.invoice_status == 'invoiced':
                    res.invoice_status = 'to invoice'
        return super(invoicefrommultisaleorder, self).unlink()

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            return {'domain':{'sale_order_id':[('partner_id','=',self.partner_id.id),('invoice_status', '=', 'to invoice')]}}

    @api.onchange('sale_order_id')
    def onechange_sale_order_id(self):
        r = []
        result = {}
        new_lines = self.env['account.invoice.line']
        for line in self.sale_order_id.order_line:
            domain = {}
            part = self.partner_id
            fpos = self.fiscal_position_id
            company = self.company_id
            currency = self.currency_id
            type = self.type

            # if not part:
            #     warning = {
            #         'title': _('Warning!'),
            #         'message': _('You must first select a partner!'),
            #     }
            #     return {'warning': warning}

            if not line.product_id:
                if type not in ('in_invoice', 'in_refund'):
                    self.price_unit = 0.0
                domain['uom_id'] = []
            else:
                if part.lang:
                    product = line.product_id.with_context(lang=part.lang)
                else:
                    product = line.product_id

                self.name = product.partner_ref
                account = self.invoice_line_ids.get_invoice_line_account(type, product, fpos, company)
                if account:
                    line.account_id = account.id

            account = self.invoice_line_ids.get_invoice_line_account(type, product, fpos, company)

            if account:
                line.account_id = account.id

            r = {
                'sale_order_id':self.sale_order_id.id,
                'origin':self.sale_order_id.name,
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_uom_qty,
                'uom_id': line.product_uom.id,
                'price_unit': line.price_unit,
                'invoice_line_tax_ids': line.tax_id,
                'price_subtotal': line.price_subtotal,
                'account_id': account.id,
            }
            new_line = new_lines.new(r)
            new_lines += new_line


        self.invoice_line_ids += new_lines
        self.env.context = dict(self.env.context, from_onechange_sale_order_id=True)
        self.sale_order_id = False
        SO_ids = self.invoice_line_ids.mapped('origin')

        result['domain'] = {'sale_order_id': [
            ('partner_id', '=', self.partner_id.id),
            ('invoice_status', '=', 'to invoice'),
            ('origin', 'not in', SO_ids),
        ]}
        return result


