# -*- coding: utf-8 -*-
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# 康虎云报表演示模块
# ver 1.2.2
#
#    Author: 康虎软件工作室(CFSoft Studio)
#    Version: 1.0
#    Create Date: 2017.02.06
#
#    Copyright (C) 2016-2017 康虎软件工作室 (<http://www.cfsoft.cf>).
#    QQ： 360026606  微信： 360026606
#
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class report_object_review(models.AbstractModel):
    """
    康虎云报表自定义报表演示模块

    本模块演示了如何通过扩展在Odoo中开发自定义模块以实现通过康虎云报表系统进行精准打印。
    参考本演示模块，实现odoo中报表精准打印的主要步骤如下：
    一、仿照本模块实现自定义报表（本步可选，也可以跳过本步，在原有QWeb报表基础上修改）
    二、在报表模板（template）文件中（xml文件， 本例为 report/report_cfprint_report_zp.xml），
        按照康虎云报表所需的格式生成json字段，生成方式参考 report_cfprint_report_zp.xml 文件及其说明

    """
    _name = 'report.report_cfprint_zp.report_object_review_zp'
    _template = 'report_cfprint_zp.report_object_review_zp'
    _description = u"支票打印模板"

    def get_records(self, model):
        """ 获取报表所需要的数据 """
        records = self.env[model].browse(self.ids)
        return records;

    @api.multi
    def render_html(self, data=None):
        """ 
        重载render_html方法，以便在报表渲染前做一些其他处理
        """
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(self._template)
        records = self.get_records(report.model)
        # cf_data = '';
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': records,
            # 'cf_data': cf_data,
        }
        return report_obj.render(self._template, docargs)
