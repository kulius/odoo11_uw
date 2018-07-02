# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SendStockSaleOrderReport(models.AbstractModel):
    _name = 'report.send_stock.template_sale_order_report'

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)

        res_doc = []
        for line in docs:
            order_doc = []
            for move_line in line.order_line:
                order_temp = {
                    'default_code': move_line.product_id.default_code,
                    'price_unit': move_line.price_unit,
                    'price_subtotal': move_line.price_subtotal,
                    'product_id': move_line.product_id.name,
                    'product_uom': move_line.product_uom.name,
                    'qty': move_line.product_uom_qty
                }
                order_doc.append(order_temp)

            temp = {
                'seller': line.user_id.name,
                'name': line.name,
                'partner_id': line.partner_id.name,
                'street': line.partner_id.street,
                'mobile': line.partner_id.mobile,
                'order_create_date': line.order_create_date,
                'order_line': order_doc
            }
            res_doc.append(temp)

        docargs = {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': res_doc,
        }
        return docargs
