# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    group_method = fields.Selection([
        ('product', 'By Product'),
        ('account', 'By Account')
    ], string='Group by', default='account',
            help="If you select 'By Product', the account move lines generated "
                 "when you validate an invoice will be "
                 "grouped by product, account, analytic account and tax code. "
                 "If you select 'By Account', they will be grouped by account, "
                 "analytic account and tax code, without taking into account "
                 "the product.")