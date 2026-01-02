# Bike Shop - Système de Gestion de Magasin de Vélos

Projet ERP développé avec Odoo 19.0 Community Edition pour gérer un magasin de vélos proposant la vente et la location de vélos.

## Description du Projet

Ce système ERP permet de gérer :
- Catalogue de produits : vélos et accessoires avec caractéristiques spécifiques
- Ventes : commandes clients avec facturation (module natif Odoo)
- Locations : contrats de location avec tarification flexible (module personnalisé)
- Gestion clients : historique des ventes et locations
- Reporting : analyses des locations et revenus

### Architecture du Projet

Le projet utilise les modules natifs Odoo (product, sale_management, stock, account) pour les fonctionnalités standards et un module personnalisé (bikeShop) pour la gestion spécifique des locations de vélos.

## Prérequis

- Python 3.10+
- PostgreSQL 12+
- Odoo 19.0 Community Edition
- Système d'exploitation : Linux (Ubuntu 24 recommandé) ou macOS

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/votre-username/bike-shop-odoo.git
cd bike-shop-odoo
```

### 2. Lancer Odoo avec le module
```bash
cd odoo/
./odoo-bin -d bikeshop_clean --addons-path=addons,../custo
```

### 3. Accéder à l'interface

Ouvrir un navigateur : http://localhost:8069

Identifiants par défaut :
- Email : admin
- Mot de passe : admin

## Partage du Projet

### Étapes pour partager le projet avec un collègue

1. **Exporter la base de données**
   - Aller sur `http://localhost:8069/web/database/manager`
   - Cliquer sur **Backup**
   - Sélectionner la base de données
   - Choisir format **zip**
   - Télécharger le fichier

2. **Envoyer au collègue**
   - Le module `bike_shop` (code source)
   - Le fichier ZIP de la base de données

3. **Le collègue place le module**
   - Mettre le dossier dans `/home/odoo/src/custo/bike_shop/`

4. **Le collègue restaure la base**
   - Aller sur `http://localhost:8069/web/database/manager`
   - Cliquer sur **Restore**
   - Uploader le ZIP de la base
   - Sélectionner **"This database is a copy"**
   - Cliquer sur **Continue**

5. **Le collègue lance Odoo**
```bash
   su - odoo
   cd /home/odoo/src/odoo
   python3 odoo-bin --addons-path=/home/odoo/src/odoo/addons,/home/odoo/src/odoo/odoo/addons,/home/odoo/src/custo -d nom_de_la_base
```

6. **Accéder au site**
   - Ouvrir `http://localhost:8069/`

## Hébergement et Déploiement

### Type d'hébergement

Local (Odoo lancé sur machine personnelle avec Docker)

### Processus d'installation

Prérequis :
- Docker et Docker Compose installés
- Git installé
- PostgreSQL

Commandes d'installation :
```bash
cd odoo/
./odoo-bin -d bikeshop_clean --addons-path=addons,../custo
```

Accès à l'interface :
- URL : http://localhost:8069
- Identifiants : admin / admin

### Limites et Risques

Limites :
- Pas de haute disponibilité (un seul serveur)
- Performances limitées par la machine locale
- Pas de sauvegarde automatique

Risques :
- Sécurité : Pas d'HTTPS en local, ne pas exposer sur Internet sans configuration SSL
- Sauvegardes : Nécessite des sauvegardes manuelles régulières de la base PostgreSQL
- Performances : Limitation selon les ressources de la machine (RAM, CPU)

Recommandations pour la production :
- Utiliser un serveur dédié (Ubuntu Server)
- Configurer HTTPS avec Let's Encrypt
- Mettre en place des sauvegardes automatiques quotidiennes
- Utiliser un reverse proxy (Nginx)

## Fonctionnalités

### Module Locations (Personnalisé)

Modèle : bike.shop.rental

Fonctionnalités principales :
- Calcul automatique de la durée et du prix selon le type de location (heure/jour/mois)
- Workflow avec boutons d'action (Confirmer, Démarrer, Retourner, Annuler)
- Génération automatique de factures
- Filtres et groupements avancés
- Reporting avec graphiques et tableaux croisés dynamiques

### Extension des Produits

Champs ajoutés au modèle product.template :
- rental_ok : Disponible à la location
- bike_type : Type de vélo (Route, VTT, Ville, Électrique)
- rental_price_hour : Tarif horaire
- rental_price_day : Tarif journalier
- rental_price_month : Tarif mensuel

### Extension des Clients

Ajouts au modèle res.partner :
- Smart button "Locations" avec compteur
- Onglet "Locations" avec historique complet
- Méthode action_view_rentals() pour filtrer les locations

## Auteur

Projet académique - 2024/2025