from odoo import http
from odoo.http import request
from datetime import datetime


class BikeShop(http.Controller):
    
    @http.route('/', type='http', auth='public', website=True)
    def homepage(self, **kwargs):
        """Page d'accueil du Bike Shop"""
        top_bikes = request.env['product.template'].sudo().search([
            ('rental_ok', '=', True)
        ], order='list_price desc', limit=3)
        
        return request.render('bike_shop.homepage', {
            'top_bikes': top_bikes,
        })
    
    @http.route('/location', type='http', auth='public', website=True)
    def location_form(self, **kwargs):
        """Page de demande de location"""
        bikes = request.env['product.template'].sudo().search([
            ('rental_ok', '=', True)
        ])
        
        return request.render('bike_shop.location_form', {
            'bikes': bikes,
        })
    
    @http.route('/location/submit', type='http', auth='public', website=True, methods=['POST'])
    def location_submit(self, **post):
        """Soumettre une demande de location"""
        bike = request.env['product.product'].sudo().browse(int(post.get('bike_id')))
        partner = request.env.user.partner_id
        
        if not partner or partner.id == request.env.ref('base.public_partner').id:
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('customer_name'),
                'email': post.get('customer_email'),
                'phone': post.get('customer_phone'),
            })
        
        start_date_str = post.get('start_date').replace('T', ' ')
        end_date_str = post.get('end_date').replace('T', ' ')
        rental_type = post.get('rental_type')
        
        # Récupérer le prix unitaire selon le type de location
        unit_price = 0.0
        if rental_type == 'hour':
            unit_price = bike.rental_price_hour
        elif rental_type == 'day':
            unit_price = bike.rental_price_day
        elif rental_type == 'month':
            unit_price = bike.rental_price_month
        
        rental = request.env['bike.shop.rental'].sudo().create({
            'partner_id': partner.id,
            'bike_id': bike.id,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'rental_type': rental_type,
            'unit_price': unit_price,
        })
        
        return request.render('bike_shop.location_thanks', {
            'rental': rental,
        })
    
    @http.route('/shop/vtt', type='http', auth='public', website=True)
    def shop_vtt(self, **kwargs):
        """Page Shop - VTT uniquement"""
        products = request.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('bike_type', '=', 'mountain')
        ])
        
        return request.render('bike_shop.shop_filtered', {
            'products': products,
            'filter_name': 'VTT',
            'filter_icon': 'fa-mountain',
        })
    
    @http.route('/shop/route', type='http', auth='public', website=True)
    def shop_route(self, **kwargs):
        """Page Shop - Vélos de route"""
        products = request.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('bike_type', '=', 'road')
        ])
        
        return request.render('bike_shop.shop_filtered', {
            'products': products,
            'filter_name': 'Vélos de Route',
            'filter_icon': 'fa-road',
        })
    
    @http.route('/shop/ville', type='http', auth='public', website=True)
    def shop_ville(self, **kwargs):
        """Page Shop - Vélos de ville"""
        products = request.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('bike_type', '=', 'city')
        ])
        
        return request.render('bike_shop.shop_filtered', {
            'products': products,
            'filter_name': 'Vélos de Ville',
            'filter_icon': 'fa-building',
        })
    
    @http.route('/shop/electrique', type='http', auth='public', website=True)
    def shop_electrique(self, **kwargs):
        """Page Shop - Vélos électriques"""
        products = request.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('bike_type', '=', 'electric')
        ])
        
        return request.render('bike_shop.shop_filtered', {
            'products': products,
            'filter_name': 'Vélos Électriques',
            'filter_icon': 'fa-bolt',
        })
    
    @http.route('/shop/location', type='http', auth='public', website=True)
    def shop_rentals(self, **kwargs):
        """Page Shop - Vélos louables uniquement"""
        products = request.env['product.template'].sudo().search([
            ('rental_ok', '=', True)
        ])
        
        return request.render('bike_shop.shop_filtered', {
            'products': products,
            'filter_name': 'Vélos en Location',
            'filter_icon': 'fa-bicycle',
        })
    
    @http.route('/about', type='http', auth='public', website=True)
    def about_page(self, **kwargs):
        """Page À propos du Bike Shop"""
        return request.render('bike_shop.about_page', {})