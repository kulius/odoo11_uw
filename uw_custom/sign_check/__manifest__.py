# -*- coding: utf-8 -*-
{
    'name': "簽口模組",
    'version': '1.0',
    'depends': [
        'account',
        'send_stock',
        'sale',
    ],
    'author': "< OdooTW  Peter Wu>",
    'website': "http://www.odootw.com/",
    'description': """
    簽口模組初版
    """,
    'data': [
        'views/sign_main_view.xml',
        'views/account_invoice_view.xml',
        'views/sale_order_view.xml',
        'views/menu.xml'
    ],
    'demo': [],
}