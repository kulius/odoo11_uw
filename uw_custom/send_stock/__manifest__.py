# -*- coding: utf-8 -*-
{
    'name': "寄倉模組與麥可客製化",
    'summary': """
    寄倉模組與麥可客製化
    """,
    'version': '1.5',
    'depends': [
        'stock',
        'sale',
        'underworld_base'
    ],
    'author': "Alltop Chia-Ming Chang",
    'website': "http://blog.alltop.com.tw/alltopco/",
    'description': """
    寄倉模組二版
    """,
    'data': [
        'views/send_stock_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/stock_picking_view.xml',
        'views/product_template_view.xml',
        'wizard/stock_out_view.xml',
        'views/group_custom_view.xml',
        'views/menu.xml',
        'report/sale_order_report_view.xml'
    ],
    'demo': [],
}