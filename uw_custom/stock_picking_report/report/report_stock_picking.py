# _*_ coding: utf-8 _*_
from odoo import models, api,fields

class ReportStockPicking(models.AbstractModel):
    _name = 'report.stock_picking_report.stock_picking_documents'

    @api.multi
    def get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)

        res_doc= []
        for line in docs:
            order_doc = []
            for move_line in line.move_lines:
                order_temp = {
                    'origin':line.origin,
                    'product_id':move_line.product_id.name,
                    'product_uom':move_line.product_uom.name,
                    'quantity_done':move_line.quantity_done
                }
                order_doc.append(order_temp)

            temp = {
                'origin':line.origin,
                'name':line.name,
                'partner_id':line.partner_id.name,
                'street':line.partner_id.street,
                'mobile':line.partner_id.mobile,
                'scheduled_date':line.scheduled_date,
                'order_line':order_doc
            }
            res_doc.append(temp)

        docargs = {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': res_doc,
        }
        return docargs