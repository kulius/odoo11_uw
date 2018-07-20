# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import UserError


class SendStockResPartner(models.Model):
    _inherit = 'res.partner'

    full_name = fields.Char(string='客戶全銜')
    saler_ids = fields.Many2many(comodel_name='res.users', string='麥可銷售員')
    group_custom_id = fields.Many2one(comodel_name='group.custom', string='群組')
