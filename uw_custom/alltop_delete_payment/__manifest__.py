# -*- coding: utf-8 -*-
{
    'name': "數立 刪除發票及支付",

    'summary': """
    可刪除己作帳支付及己付付發票，但必需先將會計相關傳票移除
    """,

    'description': """
        可刪除己作帳支付及己付付發票，但必需先將會計相關傳票移除
    """,

    'author': "數位有限公司",
    'website': "https://www.sourcelimit.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': '',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/alltop_account_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}