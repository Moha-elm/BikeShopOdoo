from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'
    
    # Lien vers les locations du client
    rental_ids = fields.One2many(
        'bike.shop.rental', 
        'partner_id', 
        string='Locations'
    )
    
    # Nombre de locations (pour affichage)
    rental_count = fields.Integer(
        string='Nombre de locations',
        compute='_compute_rental_count'
    )
    
    def _compute_rental_count(self):
        for partner in self:
            partner.rental_count = len(partner.rental_ids)
    
    def action_view_rentals(self):
        """Ouvrir les locations du client"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Locations',
            'res_model': 'bike.shop.rental',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }