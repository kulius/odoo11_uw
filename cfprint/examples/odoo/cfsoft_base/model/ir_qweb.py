# -*- coding: utf-8 -*-
##############################################################################
#
#    康虎软件 QWeb t-field 扩展
#    本类中的扩展用以实现在QWeb模板中实现自定义的展示效果
#
#    Author: 康虎软件工作室(CFSoft Studio)
#    Version: 1.0
#    Create Date: 2017.02.06
#
#    Copyright (C) 2016-2017 康虎软件工作室 (<http://www.cfsoft.cf>).
#
##############################################################################

import re
import logging
from openerp.osv import osv, orm, fields
from lxml import etree, html
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class ManyToOneRawConverter(osv.AbstractModel):
    """
    解析ManyToOne并返回不含HTML的值，
    用以替换系统自带的 <span t-field="o.partner_id" /> 指令，
    主要是对诸如：o.partner_id 的值转换成对应的名称，

    使用方法：
    <span t-field="o.partner_id" t-field-options="{&quot;widget&quot;: &quot;many2oneraw&quot;}"/>
    在原 t-field="o.partner_id" 指定中增加一个t-field-options值： {"widget": "many2oneraw"} 后即可进入该转换器
    """
    _name = 'ir.qweb.field.many2oneraw'
    _inherit = 'ir.qweb.field'

    def to_html(self, cr, uid, field_name, record, options, source_element, t_att, g_att, qweb_context, context=None):
        """ 重载父类的方法，实现只返回值内容，不要HTML的标签
        """
        _logger.info('CFSoft: Render report with ManyToOneRawConverter(to_html). ')
        try:
            content = self.record_to_html(cr, uid, field_name, record, options, context=context)
        except Exception:
            _logger.warning("Could not get field %s for model %s", field_name, record._name, exc_info=True)
            content = None

        return content;

    def record_to_html(self, cr, uid, field_name, record, options=None, context=None):
        _logger.info('CFSoft: Render report with ManyToOneRawConverter(record_to_html). ')
        [read] = record.read([field_name])
        if not read[field_name]: return ''
        _, value = read[field_name]
        return nl2br(value, options=options)

def nl2br(string, options=None):
    """
    重载source/openerp/addons/base/ir/ir_qweb.py中的同名方法，
    以实现返回原始内容，避免对内容进行HTML转换
    """
    _logger.info('CFSoft: Render report with ManyToOneRawConverter(nl2br). ')
    return string.replace('\\', '\\\\')
