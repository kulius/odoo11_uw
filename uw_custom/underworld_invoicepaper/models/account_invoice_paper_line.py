# -*- coding: utf-8 -*-
from odoo import models,fields,api

class accountinvoicepaper(models.Model):
    _inherit = "sale.order"
    _name = "account.invoice.paper.line"

    sale_order_number = fields.Char(string=u"訂單編號",related = 'sale_order_id.name')
    confirmation_date = fields.Datetime(string=u"訂購日期",related = 'sale_order_id.confirmation_date')
    customer = fields.Char(string=u"客戶",related = 'sale_order_id.partner_id.name')
    sale_order_amount = fields.Monetary(string=u"訂單金額", related = 'sale_order_id.amount_total')
    invoice_paper_id = fields.Many2one(comodel_name='account.invoice.paper')
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='銷售訂單', domain=[('invoice_status', '=', 'to invoice')])

    @api.onchange('sale_order_id')
    def onchange_partner_id(self):
        if self.invoice_paper_id.partner_id:
            return {'domain':{'sale_order_id':[('partner_id','=',self.invoice_paper_id.partner_id.id)]}}