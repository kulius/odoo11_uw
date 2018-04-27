# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.tools.float_utils import float_compare


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _get_invoice_key_cols(self):
        return [
            'partner_id', 'user_id', 'type', 'account_id', 'currency_id',
            'journal_id', 'company_id', 'partner_bank_id',
        ]

    @api.model
    def _get_invoice_line_key_cols(self):
        fields = [
            'name', 'origin', 'discount', 'invoice_line_tax_ids', 'price_unit',
            'product_id', 'account_id', 'account_analytic_id',
        ]
        for field in ['analytics_id']:
            if field in self.env['account.invoice.line']._fields:
                fields.append(field)
        return fields

    @api.model
    def _get_first_invoice_fields(self, invoice):
        return {
            'origin': '%s' % (invoice.origin or '',),
            'partner_id': invoice.partner_id.id,
            'journal_id': invoice.journal_id.id,
            'user_id': invoice.user_id.id,
            'currency_id': invoice.currency_id.id,
            'company_id': invoice.company_id.id,
            'type': invoice.type,
            'account_id': invoice.account_id.id,
            'state': 'draft',
            'reference': '%s' % (invoice.reference or '',),
            'name': '%s' % (invoice.name or '',),
            'fiscal_position_id': invoice.fiscal_position_id.id,
            'payment_term_id': invoice.payment_term_id.id,
            # 'period_id': invoice.period_id.id,
            'invoice_line_ids': {},
            'partner_bank_id': invoice.partner_bank_id.id,
        }

    @api.multi
    def do_merge(self, keep_references=True, date_invoice=False):
        """
        To merge similar type of account invoices.
        Invoices will only be merged if:
        * Account invoices are in draft
        * Account invoices belong to the same partner
        * Account invoices are have same company, partner, address, currency,
          journal, currency, salesman, account, type
        Lines will only be merged if:
        * Invoice lines are exactly the same except for the quantity and unit

         @param self: The object pointer.
         @param keep_references: If True, keep reference of original invoices

         @return: new account invoice id

        """

        new_invoice = None
        date_due = None
        origin = None
        reference = None
        for invoice in self:
            if not new_invoice or new_invoice.date_invoice > invoice.date_invoice: # date_invoice 發票日期
                new_invoice = invoice # 發票日期挑最後的
            if not date_due or new_invoice.date_due < invoice.date_due: # date_due 到期日期
                date_due = invoice.date_due # 到期日期挑最早的

            if keep_references:
                if not origin: # 如果來源訂單編號是空的話, 則將來源訂單編號寫入
                    origin = invoice.origin
                else:
                    origin = origin + ' ' + invoice.origin # 來源訂單編號
                if not reference:
                    reference = invoice.reference
                else:
                    reference = reference + ' ' + invoice.reference # 供應商編號

        for invoice in self:
            if new_invoice != invoice:
                add_ids = [(4, l.id) for l in invoice.invoice_line_ids] # 將 id 的現有記錄添加至集合 (無法直接在one2many使用)
                new_invoice.write({'invoice_line_ids': add_ids}) # 將集合寫入one2many
                invoice.unlink() # 將原本的發票刪除
        if keep_references:
            new_invoice.write({'date_due': date_due,
                               'origin': origin,
                               'reference': reference}) # 在新創的發票中, 寫入發票的到期日期, 訂單編號, 供應商編號
        else:
            new_invoice.write({'date_due': date_due})
        new_invoice.merge_lines() # 合併每張發票(僅限草稿狀態)的發票明細
        return new_invoice.id

    @api.multi
    def merge_lines(self):
        self.ensure_one()
        to_delete = []
        itered = []
        for line in self.invoice_line_ids:
            itered.append(line.id) # 將發票明細的記錄寫入陣列
            line_to_merge = self.invoice_line_ids.search([('invoice_id', '=', self.id),
                                                      ('discount', '=', line.discount), # 折扣
                                                      # ('invoice_line_tax_id', '=', line.invoice_line_tax_id.id),
                                                      ('price_unit', '=', line.price_unit), # 單價
                                                      ('product_id', '=', line.product_id.id), # 產品
                                                      ('account_id', '=', line.account_id.id), # 科目
                                                      ('account_analytic_id', '=', line.account_analytic_id.id), # 允許使用輔助核算項
                                                      ('id', 'not in', itered)], limit=1) # 確保搜尋出來的資料只會有一筆且不會重複
            if line_to_merge:
                to_delete.append(line.id) # 準備刪除相同產品的明細
                line_to_merge.write({'quantity': line_to_merge.quantity + line.quantity,
                                     'origin': line_to_merge.origin + line.origin if (
                                     line_to_merge.origin and line.origin) else False}) # Quantity :數量 (過濾相同產品的明細, 並將產品的數量更新)
        self.write({'invoice_line_ids': [(2, x, 0) for x in to_delete]}) # 從集合中刪除 id 的記錄，然後刪除它(從資料庫中)


    # Load all unsold PO lines
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        if not self.purchase_id:
            return {}
        if not self.partner_id:
            self.partner_id = self.purchase_id.partner_id.id

        new_lines = self.env['account.invoice.line']
        for line in self.purchase_id.order_line:
            # Load a PO line only once
            if line in self.invoice_line_ids.mapped('purchase_line_id'):
                continue
            if line.product_id.purchase_method == 'purchase':
                qty = line.product_qty - line.qty_invoiced
            else:
                qty = line.qty_received - line.qty_invoiced
            if float_compare(qty, 0.0, precision_rounding=line.product_uom.rounding) <= 0:
                qty = 0.0
            product_exists = [x for x in new_lines.filtered(lambda l: l.product_id.id == line.product_id.id and \
                                                                      l.price_unit == line.price_unit)]
            if product_exists:
                product_exists[0].quantity = product_exists[0].quantity + qty
            else:
                taxes = line.taxes_id
                invoice_line_tax_ids = self.purchase_id.fiscal_position_id.map_tax(taxes)
                data = {
                    'purchase_line_id': line.id,
                    'name': self.purchase_id.name + ': ' + line.name,
                    'origin': self.purchase_id.origin,
                    'uom_id': line.product_uom.id,
                    'product_id': line.product_id.id,
                    'account_id': self.env['account.invoice.line'].with_context(
                        {'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
                    'price_unit': line.order_id.currency_id.compute(line.price_unit, self.currency_id, round=False),
                    'quantity': qty,
                    'discount': 0.0,
                    'account_analytic_id': line.account_analytic_id.id,
                    'analytic_tag_ids': line.analytic_tag_ids.ids,
                    'invoice_line_tax_ids': invoice_line_tax_ids.ids
                }
                account = new_lines.get_invoice_line_account('in_invoice', line.product_id,
                                                             self.purchase_id.fiscal_position_id,
                                                             self.env.user.company_id)
                if account:
                    data['account_id'] = account.id
                new_line = new_lines.new(data)
                new_line._set_additional_fields(self)
                new_lines += new_line

        self.invoice_line_ids += new_lines
        self.purchase_id = False
        return {}


    def inv_line_characteristic_hashcode(self, invoice_line):
        """Inherit the native method that generate hashcodes for grouping.
        When grouping per account, we remove the product_id from
        the hashcode.
        WARNING: I suppose that the other methods that inherit this
        method add data on the end of the hashcode, not at the beginning.
        This is the case of github/OCA/account-closing/
        account_cutoff_prepaid/account.py"""
        res = super(AccountInvoice, self).inv_line_characteristic_hashcode(
            invoice_line)
        if self.journal_id.group_method == 'account':
            hash_list = res.split('-')
            # remove product_id from hashcode
            hash_list.pop(2)
            res = '-'.join(hash_list)
        return res