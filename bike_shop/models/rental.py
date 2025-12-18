from odoo import models, fields, api
from odoo.exceptions import UserError


class Rental(models.Model):
    _name = 'bike.shop.rental'
    _description = 'Contrat de location'
    _rec_name = 'reference'
    
    # Référence et client
    reference = fields.Char(string='Référence', required=True, copy=False, readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    
    # Vélo loué
    bike_id = fields.Many2one('product.product', string='Vélo', required=True, 
                               domain=[('rental_ok', '=', True)])
    
    # Dates et période
    start_date = fields.Datetime(string='Date de début', required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(string='Date de fin', required=True)
    duration_days = fields.Float(string='Durée (jours)', compute='_compute_duration', store=True)
    
    # Prix
    rental_type = fields.Selection([
        ('hour', 'Heure'),
        ('day', 'Jour'),
        ('month', 'Mois'),
    ], string='Type de location', required=True, default='day')
    unit_price = fields.Float(string='Prix unitaire', digits=(10, 2))
    total_price = fields.Float(string='Prix total', compute='_compute_total_price', store=True)
    
    # Statut
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('ongoing', 'En cours'),
        ('returned', 'Retourné'),
        ('cancelled', 'Annulé'),
    ], string='État', default='draft', required=True)
    
    # Lien vers la facture
    invoice_id = fields.Many2one('account.move', string='Facture', readonly=True, copy=False)
    invoice_status = fields.Selection([
        ('no', 'Pas de facture'),
        ('to_invoice', 'À facturer'),
        ('invoiced', 'Facturé'),
    ], string='Statut facturation', default='no', compute='_compute_invoice_status', store=True)
    
    # Génération automatique de la référence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('bike.shop.rental') or 'New'
        return super(Rental, self).create(vals_list)
    
    # Calcul de la durée
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.duration_days = delta.total_seconds() / 86400
            else:
                record.duration_days = 0
    
    # Calcul du prix total
    @api.depends('rental_type', 'unit_price', 'duration_days')
    def _compute_total_price(self):
        for record in self:
            if record.rental_type == 'hour':
                record.total_price = record.unit_price * (record.duration_days * 24)
            elif record.rental_type == 'day':
                record.total_price = record.unit_price * record.duration_days
            elif record.rental_type == 'month':
                record.total_price = record.unit_price * (record.duration_days / 30)
            else:
                record.total_price = 0
    
    # Calcul du statut de facturation
    @api.depends('invoice_id', 'state')
    def _compute_invoice_status(self):
        for record in self:
            if record.invoice_id:
                record.invoice_status = 'invoiced'
            elif record.state in ['confirmed', 'ongoing', 'returned']:
                record.invoice_status = 'to_invoice'
            else:
                record.invoice_status = 'no'
    
    # AUTOMATISATION : Remplir le prix unitaire selon le vélo et le type
    @api.onchange('bike_id', 'rental_type')
    def _onchange_bike_rental_type(self):
        if self.bike_id and self.rental_type:
            if self.rental_type == 'hour':
                self.unit_price = self.bike_id.rental_price_hour or 0
            elif self.rental_type == 'day':
                self.unit_price = self.bike_id.rental_price_day or 0
            elif self.rental_type == 'month':
                self.unit_price = self.bike_id.rental_price_month or 0
    
    # ========== BOUTONS D'ACTION ==========
    
    def action_confirm(self):
        """Confirmer la location"""
        self.write({'state': 'confirmed'})
    
    def action_start(self):
        """Démarrer la location"""
        self.write({'state': 'ongoing'})
    
    def action_return(self):
        """Marquer le vélo comme retourné"""
        self.write({'state': 'returned'})
    
    def action_cancel(self):
        """Annuler la location"""
        self.write({'state': 'cancelled'})
    
    def action_create_invoice(self):
        """Créer une facture pour cette location"""
        self.ensure_one()
        
        # Vérifier qu'il n'y a pas déjà une facture
        if self.invoice_id:
            raise UserError("Une facture existe déjà pour cette location.")
        
        # Créer la facture
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f'Location {self.bike_id.name} - {self.reference}',
                'quantity': 1,
                'price_unit': self.total_price,
            })],
        })
        
        # Lier la facture à la location
        self.invoice_id = invoice.id
        
        # Ouvrir la facture
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_view_invoice(self):
        """Voir la facture associée"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'target': 'current',
        }