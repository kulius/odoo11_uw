# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class SendStockStockPicking(models.Model):
    _inherit = 'stock.picking'

    driver_id = fields.Many2one(comodel_name='res.users', string='出貨司機')
