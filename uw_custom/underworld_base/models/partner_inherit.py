# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models,fields,api
from odoo.exceptions import UserError


class uwpartnerinherit(models.Model):
    _inherit = "res.partner"


    city_zone = fields.Char(string=u"區域")
    cus_kind = fields.Char(string=u"客戶屬性")
    bus_time = fields.Char(string=u"營業時間")
    bus_day = fields.Char(string=u"營業日")
    fax = fields.Char(string=u"傳真")
    sno = fields.Char(string=u"統編")
    vat = fields.Char(string=u"國際稅碼(統編)")
    cus_no = fields.Char(string=u"客編")
    cus_sales = fields.Char(string=u"業務")
    comment1 = fields.Text(string=u"其他備註")

    @api.multi
    def name_get(self):
        result = []
        for myrec in self:
            if not myrec.name:
               myname = '-'
            else:
               myname = myrec.name
            if not myrec.cus_no:
               mycusno = '-'
            else:
               mycusno = myrec.cus_no
            mypartner = "%s (%s)" % (myname,mycusno)
            result.append((myrec.id, mypartner))
        return result

