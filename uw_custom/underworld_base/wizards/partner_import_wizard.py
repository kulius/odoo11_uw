# -*- coding: utf-8 -*-
# Author : Peter Wu

import base64
import xlrd
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
#import sys
#import importlib

XL_CELL_EMPTY = 0
XL_CELL_TEXT = 1
XL_CELL_NUMBER = 2
XL_CELL_DATE = 3
XL_CELL_BOOLEAN = 4
XL_CELL_ERROR = 5
XL_CELL_BLANK = 6


class partnerimportwizard(models.TransientModel):
    _name = "underworld_base.partner_import_wizard"

    excel_file = fields.Binary(string=u"上傳EXCEL檔案")
    start_row = fields.Integer(size=3, string=u"啟始ROW", default=2)
    end_row = fields.Integer(size=3, string=u"結止ROW", default=2)
    # auto_finish = fields.Boolean(string=u"項次自動編號", default=True)

    def partner_action_import(self):
        if self.start_row == 1 :
            raise UserError(u"數值錯誤,ROW啟始數值從 2 開始")
        if self.start_row < 0 or self.end_row < 0:
            raise UserError(u"數值錯誤,ROW數值不能小於0")
        if self.start_row > self.end_row:
            raise UserError(u"數值錯誤,啟始ROW數值大於結止ROW")

        if not self.excel_file:
            raise UserError(u"檔案錯誤,沒有上傳正確的Excel File")
        xls = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = xls.sheet_by_index(0)
        if self.start_row > 0 or self.end_row > 0:
            nstartrow = self.start_row
            if self.end_row > sheet.nrows:
               nendrow = sheet.nrows
            else:
               nendrow = self.end_row
        else:
            nstartrow = 2
            nendrow = sheet.nrows
            # print "%s" % nendrow
        #importlib.reload(sys)

        #sys.setdefaultencoding('utf-8')
        self.ensure_one()
        partner_rec = self.env['res.partner']

        if not self.excel_file:
            raise UserError(u"沒有上傳正確的Excel File")
        #xls = xlrd.open_workbook(file_contents=base64.encodestring(self.excel_file))
        xls = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = xls.sheet_by_index(0)
        # nstartrow = 1
        # nendrow = sheet.nrows

        for row in range(nstartrow -1, nendrow):

            cell = sheet.cell(row, 1)
            mycusno = '-'
            if cell.ctype == XL_CELL_EMPTY:
               continue
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
               mycusno = u'' + str((cell.value))  # 客編
            #print ('%s' % mycusno)

            cell = sheet.cell(row, 2)
            myname = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
                myname = u'' + str((cell.value))  # 客戶名稱
            #print ('%s' % myname)

            cell = sheet.cell(row, 3)
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
                mykind = u'' + str((cell.value))  # 客戶類別
            else:
                mykind = '-'
            # print "3:%s" % mysitemdesc

            cell = sheet.cell(row, 4)
            mycity = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
                mycity = u'' + str((cell.value))      # 城市


            cell = sheet.cell(row, 5)
            mycityzone = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
                mycityzone = u''+ str((cell.value))   # 區域


            cell = sheet.cell(row, 6)
            myaddress = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
                myaddress = u'' + str((cell.value))  # 地址

            cell = sheet.cell(row, 7)
            mybustime = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mybustime = u'' + str((cell.value))  # 營業時間

            cell = sheet.cell(row, 8)
            mybusday = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mybusday = u'' + str((cell.value))  # 營業日

            cell = sheet.cell(row, 9)
            myzipcode = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                myzipcode = u'' + str((cell.value))  # ZIP

            ## 10 zone  不需要

            cell = sheet.cell(row, 11)
            myphone = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                myphone = u'' + str((cell.value))  # 電話

            cell = sheet.cell(row, 12)
            mycellphone = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mycellphone = u'' + str((cell.value))  # 行動電話

            cell = sheet.cell(row, 13)
            myfax = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                myfax = u'' + str((cell.value))  # 傳真

            cell = sheet.cell(row, 14)
            myid = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                myid = u'' + str((cell.value))  # 統編

            cell = sheet.cell(row, 15)
            mycontact = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mycontact = u'' + str((cell.value))  # 連絡人

            ## 16 mid 不需要

            cell = sheet.cell(row, 17)
            mysales = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mysales = u'' + str((cell.value))  # 業務員

            ## 18 sales_code 不需要
            ## 19 reserve 不需要
            ## 20 key_date 不需要
            ## 21 valid 不需要
            ## 22 close 不需要

            cell = sheet.cell(row, 23)
            mymemo = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mymemo = u'' + str((cell.value))  # 備註

            cell = sheet.cell(row, 24)
            mymemo1 = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mymemo1 = u'' + str((cell.value))  # 其他備註


            myparid = partner_rec.create({'cus_no':mycusno,'name':myname,'cus_kind': mykind,'city':mycity,
                                          'city_zone':mycityzone,'street':myaddress,'bus_time':mybustime,
                                          'bus_day':mybusday,'zip':myzipcode,'phone':myphone,'mobile':mycellphone,
                                          'fax':myfax,'vat':myid,'cus_sales':mysales,'comment':mymemo,
                                          'comment1':mymemo1,'company_type':'company','invoice_warn':'no-message',
                                          'picking_warn':'no-message','purchase_warn':'no-message',
                                          'sale_warn':'no-message','customer':True,'supplier':False})
            #print('%s' % myparid.id)
            if mycontact != '-':
                partner_rec.create({'parent_id':myparid.id,'company_type':'person','name':mycontact,'mobile':mycellphone,
                                    'phone':myphone,'street':myaddress,'invoice_warn':'no-message','picking_warn':'no-message',
                                    'purchase_warn':'no-message','sale_warn':'no-message'})



