from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # Champs spécifiques pour la location de vélos
    rental_ok = fields.Boolean(string='Disponible à la location', default=False)
    
    # Type de vélo
    bike_type = fields.Selection([
        ('road', 'Route'),
        ('mountain', 'VTT'),
        ('city', 'Ville'),
        ('electric', 'Électrique'),
    ], string='Type de vélo')
    
    # Tarifs de location
    rental_price_hour = fields.Float(string='Tarif location/heure', digits='Product Price')
    rental_price_day = fields.Float(string='Tarif location/jour', digits='Product Price')
    rental_price_month = fields.Float(string='Tarif location/mois', digits='Product Price')


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    # Les champs related pour accéder facilement depuis product.product
    rental_ok = fields.Boolean(related='product_tmpl_id.rental_ok', store=True, readonly=False)
    bike_type = fields.Selection(related='product_tmpl_id.bike_type', store=True, readonly=False)
    rental_price_hour = fields.Float(related='product_tmpl_id.rental_price_hour', store=True, readonly=False)
    rental_price_day = fields.Float(related='product_tmpl_id.rental_price_day', store=True, readonly=False)
    rental_price_month = fields.Float(related='product_tmpl_id.rental_price_month', store=True, readonly=False)