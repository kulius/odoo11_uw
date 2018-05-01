# -*- coding: utf-8 -*-
from openerp import http

# class CfsoftBase(http.Controller):
#     @http.route('/cfsoft_base/cfsoft_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cfsoft_base/cfsoft_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cfsoft_base.listing', {
#             'root': '/cfsoft_base/cfsoft_base',
#             'objects': http.request.env['cfsoft_base.cfsoft_base'].search([]),
#         })

#     @http.route('/cfsoft_base/cfsoft_base/objects/<model("cfsoft_base.cfsoft_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cfsoft_base.object', {
#             'object': obj
#         })