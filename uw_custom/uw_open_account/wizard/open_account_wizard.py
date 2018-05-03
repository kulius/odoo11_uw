# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class OpenAccountWizard(models.TransientModel):
    _name = 'open.account.wizard'

    oa_date = fields.Date(string='月結日期', required=True)

    def filtered_account_invoice(self):

        return {
            'name': self.oa_date + '的月結單',
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'view_mode': 'tree,form',
            'domain': [('state', 'in', ['draft', 'open']), ('date_invoice', '<=', self.oa_date)],
            'target': 'current'
        }
