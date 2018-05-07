# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SendStockMain(models.Model):
    _inherit = 'stock.picking'

    location_dest_id = fields.Many2one(readonly=False,states={})


# class SendStockMain(models.Model):
#     _name = 'send.stock.main'
#
#     name = fields.Char(string='參考')
#     partner_id = fields.Many2one(comodel_name='res.partner', string='業務夥伴')
#     location_sou_id = fields.Many2one(comodel_name='stock.location', string='來源位置')
#     location_des_id = fields.Many2one(comodel_name='stock.location', string='目的位置')
#     scheduled_date = fields.Date(string='預定交貨日期')
#     move_lines = fields.One2many(comodel_name='send.stock.line', inverse_name='send_id')
#     state = fields.Selection(selection=[('draft', '草稿'), ('assigned', '就緒'), ('done', '完成')])
#
#
# class SendStockLine(models.Model):
#     _name = 'send.stock.line'
#
#     send_id = fields.Many2one(comodel_name='send.stock.main', string='源主檔')
#     product_id = fields.Many2one(comodel_name='product.product', string='產品')
#     qty = fields.Float(string='數量')
