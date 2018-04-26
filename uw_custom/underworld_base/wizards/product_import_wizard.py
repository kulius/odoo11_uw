# -*- coding: utf-8 -*-
# Author : Peter Wu


# -*- coding: utf-8 -*-
# Author : Peter Wu


import base64
import xlrd
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


XL_CELL_EMPTY = 0
XL_CELL_TEXT = 1
XL_CELL_NUMBER = 2
XL_CELL_DATE = 3
XL_CELL_BOOLEAN = 4
XL_CELL_ERROR = 5
XL_CELL_BLANK = 6


class prodimportwizard(models.TransientModel):
    _name = "underworld_base.prod_import_wizard"

    excel_file = fields.Binary(string=u"上傳EXCEL檔案")
    excel_sheet_num = fields.Integer(string=u"工作底稿序號",default=0)
    start_row = fields.Integer(size=3, string=u"啟始ROW", default=2)
    end_row = fields.Integer(size=3, string=u"結止ROW", default=2)



    def prod_action_import(self):
        if self.start_row == 1 :
            raise UserError(u"數值錯誤,ROW啟始數值從 2 開始")
        if self.start_row < 2 or self.end_row < 2:
            raise UserError(u"數值錯誤,ROW數值不能小於2")
        if self.start_row > self.end_row:
            raise UserError(u"數值錯誤,啟始ROW數值大於結止ROW")

        if not self.excel_file:
            raise UserError(u"檔案錯誤,沒有上傳正確的Excel File")
        xls = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = xls.sheet_by_index(self.excel_sheet_num)
        if self.start_row > 1 or self.end_row > 1:
            nstartrow = self.start_row
            if self.end_row > sheet.nrows:
               nendrow = sheet.nrows
            else:
               nendrow = self.end_row
        else:
            nstartrow = 2
            nendrow = sheet.nrows

        #self.ensure_one()
       
        if not self.excel_file:
            raise UserError(u"沒有上傳正確的Excel File")

        for row in range(nstartrow -1, nendrow):

            cell = sheet.cell(row, 0)
            myproductno = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
               myproductno = u'' + str((cell.value))                      # PROD 產品代號


            cell = sheet.cell(row, 1)
            myproductcateg = '-'
            codeloc1=0
            codeloc2=0
            codeloc3=0
            myparentid = 1
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
               myname = u'' + str((cell.value))                           # PROD 產品分類
               startn = 0
               endn = len(myname)
               codeloc1 = myname.find('-',0,len(myname))
               myname1 = u''+ myname[0:(codeloc1)]
               myname11 = u''+ myname[((codeloc1)+1):len(myname)]
               mycompletename = u"All / "
               print("codeloc1:%s" % codeloc1)
               print("myname1:%s" % myname1)
               print("myname11:%s" % myname11)
               mycompletename = mycompletename + myname1
               print("complelename1:%s" % mycompletename)
               print("myname1:%s" % myname1)
               print("parentid1:%s" % myparentid)
               myrec = self.env['product.category'].search([('name', 'ilike', myname1), ('parent_id', '=', 1)])
               if not myrec:
                  try :
                     myrec.create({'name':myname1,'complete_name':mycompletename,'parent_id': 1})
                  except ValueError:
                     print("NO CREATE CATEGORY:%s" % myname1)
               myid2 = self.env['product.category'].search([('name','ilike',myname1),('parent_id','=',1)])
               codeloc2 = myname11.find('-',0,len(myname11))
               myname2 = u''+ myname11[0:codeloc2]
               myname21 = u'' + myname11[(codeloc2+1):len(myname11)]
               print("codeloc2:%s" % codeloc2)
               print("myname2:%s" % myname2)
               print("myname21:%s" % myname21)
               mycompletename = mycompletename + " / " + myname2
               print("complelename2:%s" % mycompletename)
               print("myname2:%s" % myname2)
               if len(myid2) >= 2:
                  print("parentid2:%s" % myid2[0].id)
                  myid2_value=myid2[0].id
               else:
                  print("parentid2:%s" % myid2.id)
                  myid2_value = myid2.id
               myrec = self.env['product.category'].search([('name','ilike',myname2),('parent_id','=',myid2_value)])
               if not myrec:
                  try :
                     myrec.create({'name': myname2, 'complete_name': mycompletename, 'parent_id': myid2_value})
                  except ValueError:
                     print("NO CREATE CATEGORY:%s" % myname2)
               myid3 = self.env['product.category'].search([('name','ilike',myname2),('parent_id','=',myid2_value)])
               #codeloc3 = myname21.find('-',0,len(myname21))
               myname3 = myname21
               #myname3 = u'' + myname21[0:codeloc3]
               #myname31 = u'' + myname21[(codeloc3+1):len(myname21)]
               #print("codeloc3:%s" % codeloc3)
               print("myname3:%s" % myname3)
               #print("myname31:%s" % myname31)
               mycompletename = mycompletename + " / " + myname3
               print("complelename3:%s" % mycompletename)
               print("myname3:%s" % myname3)
               if len(myid3) >= 2 :
                  print("parentid3:%s" % myid3[0].id)
                  myid3_value = myid3[0].id
               else:
                  print("parentid3:%s" % myid3.id)
                  myid3_value = myid3.id
               myrec = self.env['product.category'].search([('name', 'ilike', myname3), ('parent_id', '=', myid3_value)])
               if not myrec:
                  try :
                     myrec.create({'name': myname3, 'complete_name': mycompletename, 'parent_id': myid3_value})
                  except ValueError:
                     print ("NO CREATE CATEGORY:%s" % myname3)
               myid4 = self.env['product.category'].search([('name','ilike',myname3),('parent_id','=',myid3_value)])

            cell = sheet.cell(row, 2)
            myprodbrand = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
               myprodbrand = u''+ str((cell.value))                        # PROD 產品品牌


            cell = sheet.cell(row, 3)
            mysupplier = '-'
            mysuppid = 1
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
               mysupplier = u''+str((cell.value))                        #  PROD 產品供應商
               if mysupplier:
                  mysupplierdata = self.env['res.partner'].search([('name','ilike',mysupplier)])
                  if not mysupplierdata :
                     try :
                         myrecid = self.env['res.partner'].create({'name':mysupplier,'picking_warn':'no-message','purchase_warn':'no-message',
                                                               'sale_warn':'no-message','customer':False,'supplier':True})
                         mysuppid = myrecid.id
                     except ValueError:
                         mysuppid = 1
                  else:
                     if len(mysupplierdata) >= 2 :
                        mysuppid = mysupplierdata[0].id
                     else:
                        mysuppid = mysupplierdata.id



            cell = sheet.cell(row, 4)
            myname = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
               myname = u''+str((cell.value))                            #  PROD 產品品名


            cell = sheet.cell(row, 5)
            myenname = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
                myenname = str((cell.value))                         #  PROD 英文品名

            print("EN_NAME:%s" % myenname)

            cell = sheet.cell(row, 6)
            myproductspec = '-'
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
               myproductspec = u'' + str((cell.value))                   # PROD 產品規格


            cell = sheet.cell(row, 7)
            mybarcode = ''
            if cell.ctype in (XL_CELL_TEXT,XL_CELL_NUMBER):
                mybarcode = u''+str((cell.value))                        # PROD 國際條碼
                mycount = self.env['product.template'].search_count([('barcode','=',mybarcode)])
                if mycount > 0 :
                   mybarcode = ''

            cell = sheet.cell(row, 8)
            mywholesaleprice = '0'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mywholesaleprice = float(str((cell.value)))               # PROD 產品批發價

            cell = sheet.cell(row, 9)
            mylistprice = '0'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mylistprice = float(str(cell.value))                      # PROD 產品零售價


            cell = sheet.cell(row, 10)
            mydescription = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                mydescription = u'' + str((cell.value))                   # PROD 產品查詢參照
            myprodrec1 = self.env['product.product']
            myprodrec = self.env['product.template'].search([('name','=',myname),('product_spec','=',myproductspec)])
            if not myprodrec:
               if mybarcode=='':
                   try:
                       myid = myprodrec.create(
                           {'default_code': 'product_no', 'product_no': myproductno, 'categ_id': myid4.id,
                            'product_brand': myprodbrand, 'name': myname,
                            'en_name': myenname, 'product_spec': myproductspec, 'wholesale_price': mywholesaleprice,
                            'list_price': mylistprice, 'product_memo': mydescription, 'responsible_id': 1,
                            'type': 'product', 'uom_id': 1, 'uom_po_id': 1,
                            'purchase_line_warn': 'no-message', 'sale_line_warn': 'no-message', 'tracking': 'none',
                            'sale_ok': True, 'purchase_ok': True,
                            'variant_seller_ids': [
                                (0, 0, {'name': mysuppid, 'delay': 14, 'min_qty': 1, 'price': 0})], })
                       myprodrec1.create({'product_tmpl_id': myid.id, 'active': True})
                   except ValueError:
                       print("Create %s" % myname)
               else:
                   try:
                       myid = myprodrec.create(
                           {'default_code': 'product_no', 'product_no': myproductno, 'categ_id': myid4.id,
                            'product_brand': myprodbrand, 'name': myname,
                            'en_name': myenname, 'product_spec': myproductspec, 'wholesale_price': mywholesaleprice,
                            'barcode': mybarcode,
                            'list_price': mylistprice, 'product_memo': mydescription, 'responsible_id': 1,
                            'type': 'product', 'uom_id': 1, 'uom_po_id': 1,
                            'purchase_line_warn': 'no-message', 'sale_line_warn': 'no-message', 'tracking': 'none',
                            'sale_ok': True, 'purchase_ok': True,
                            'variant_seller_ids': [
                                (0, 0, {'name': mysuppid, 'delay': 14, 'min_qty': 1, 'price': 0})], })
                       myprodrec1.create({'product_tmpl_id': myid.id, 'active': True})
                   except ValueError:
                       print("Create %s" % myname)




