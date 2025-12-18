# from odoo import http


# class BikeShop(http.Controller):
#     @http.route('/bike_shop/bike_shop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bike_shop/bike_shop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bike_shop.listing', {
#             'root': '/bike_shop/bike_shop',
#             'objects': http.request.env['bike_shop.bike_shop'].search([]),
#         })

#     @http.route('/bike_shop/bike_shop/objects/<model("bike_shop.bike_shop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bike_shop.object', {
#             'object': obj
#         })

