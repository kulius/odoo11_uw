# -*- coding: utf-8 -*-
{
    'name': "CFSoft Base Module（康虎基础模块）",

    'summary': """
        康虎软件基础模块
        """,

    'description': """
        本模块是康虎工作室所开发相关模块的基础模块，该模块中实现一些通用的基础功能。
    """,

    'author': "CFsoft Studio",
    'website': "http://www.cfsoft.cf",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'CFSoft',
    'version': '1.2.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'view/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'data/demo.xml',
    ],
}