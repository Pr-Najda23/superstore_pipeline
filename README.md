#  Avito Real Estate Data Pipeline

## Contexte

Avito.ma est une plateforme majeure d’annonces immobilières au Maroc. Les données disponibles sont souvent non structurées et nécessitent un traitement avant toute analyse.

Ce projet consiste à construire un **pipeline de données complet** permettant de transformer des données brutes issues du scraping en datasets exploitables pour :

* Business Intelligence (Power BI)
*  Machine Learning

---

##  Architecture du Pipeline

```
Source → Extract → Staging → Clean → Data Warehouse
```

Deux schémas sont générés :

### BI Schema (`bi_schema`)

* Modèle dimensionnel (Star Schema)
* Tables :

  * Fact_Annonce
  * Dim_Temps
  * Dim_Localisation
  * Dim_Caracteristiques
* Utilisation : reporting & dashboards (Power BI)

### ML Schema (`ml_schema`)

* One Big Table (OBT)
* Dataset plat avec toutes les features
* Utilisation : Machine Learning

---

## Étapes du Pipeline

### 1. Extract

* Scraping des annonces immobilières depuis Avito.ma
* Données collectées :

  * Titre, prix, ville, surface, chambres, etc.
  * Exclusion des données personnelles (RGPD)

---

### 2. Staging

* Stockage des données brutes
* Gestion :

  * Pagination
  * Logs
  * Erreurs scraping

---

### 3. Clean

* Suppression des doublons
* Gestion des valeurs manquantes
* Standardisation (villes, formats)
* Correction des types de données

---

### 4. Feature Engineering

* Prix par m²
* Âge du bien
* Variables géographiques

---

### 5. Data Warehouse

* Chargement dans :

  * `bi_schema`
  * `ml_schema`
* Optimisation :

  * Index
  * Relations

---

## Conformité des données

* Respect des conditions d’utilisation d’Avito.ma
* Minimisation des données
* Suppression des informations sensibles
* Respect des principes RGPD

---

## Technologies utilisées

* Python (Pandas, Selenium)
* SQL (PostgreSQL / SQL Server)
* Docker Compose
* Power BI


