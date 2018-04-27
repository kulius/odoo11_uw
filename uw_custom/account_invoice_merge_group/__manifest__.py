# -*- coding: utf-8 -*-
{
    'name': 'Account Invoice Merge',
    'version': '8.0.1.1.1',
    'category': 'Finance',
    'author': "Elico Corp,Odoo Community Association (OCA), Jason(jaronemo@msn.com)",
    'website': 'http://www.openerp.net.cn',
    'license': 'AGPL-3',
    'depends': ['account','sale', 'purchase'],
    'data': [
        'wizard/invoice_merge_view.xml',
        'invoice_view.xml',
        'account_view.xml',
    ],
    'test': [
    ],
    'demo': [],
    'installable': True,
    'active': False,
    'certificate': False,
}