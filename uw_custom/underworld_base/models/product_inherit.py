# -*- coding: utf-8 -*-
# Author : Peter Wu


from odoo import models,fields,api
from odoo.exceptions import UserError


class productinherit(models.Model):
    _inherit = "product.template"

    product_no = fields.Char(string=u"產品代號")
    product_brand = fields.Char(string=u"品牌")
    en_name = fields.Char(string=u"英文品名")
    product_spec = fields.Char(string=u"產品規格")
    wholesale_price = fields.Float(digits=(10,2),string=u"批發價")
    product_memo = fields.Char(string=u"產品參照")


    @api.multi
    def name_get(self):
        result = []
        for myrec in self:
            if not myrec.name:
                myname = '-'
            else:
                myname = myrec.name
            if not myrec.product_no:
                myprodno = '-'
            else:
                myprodno = myrec.product_no
            myproduct = "%s (%s)" % (myname, myprodno)
            result.append((myrec.id, myproduct))
        return result

