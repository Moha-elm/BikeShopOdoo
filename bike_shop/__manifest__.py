{
    'name': "Bike Shop - Vente & Location",
    'summary': "Gestion de magasin de vélos : vente et location",
    'description': """
        Système de gestion pour magasin de vélos incluant :
        - Vente de vélos et accessoires (modules natifs Odoo)
        - Location de vélos (module personnalisé)
        - Gestion clients et contrats
    """,
    'author': "Votre Nom",
    'website': "https://github.com/votre-repo",
    'category': 'Sales',
    'version': '2.0',
    'depends': [
        'base',
        'contacts',
        'product',
        'sale_management',
        'stock',
    ],
    'data': [
    'security/ir.model.access.csv',
    'data/rental_sequence.xml',
    'views/product_views.xml',
    'views/rental_views.xml',
    'views/rental_report_views.xml',
    'views/partner_views.xml',
    'views/templates.xml',
    'demo/demo.xml',
     # Données de démonstration (dans data pour qu'elles se rechargent)
],
    'demo': [
        # Vide - on met les données demo dans 'data' pour ce projet
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}