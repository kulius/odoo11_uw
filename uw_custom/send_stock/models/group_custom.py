# _*_ coding: utf-8 _*_
from odoo import models, api,fields


class GroupCustom(models.Model):
    _name = 'group.custom'

    name = fields.Char(string='群組名稱')


class GroupProduct(models.Model):
    _name = 'group.product'

    name = fields.Char(string='群組名稱')
