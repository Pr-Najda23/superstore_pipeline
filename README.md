🏠 Avito Real Estate Data Pipeline & Machine Learning Project
📌 Contexte du projet

Ce projet consiste à concevoir un pipeline de données industriel complet autour des annonces immobilières publiées sur la plateforme Avito.ma.

Les données collectées sont souvent hétérogènes, semi-structurées et nécessitent plusieurs étapes de transformation avant d’être exploitables pour :

📊 L’analyse décisionnelle (Power BI)
🤖 Le Machine Learning

Le projet suit une architecture moderne de type :

Source → Extract → Staging → Clean → Warehouse → BI / ML

L’objectif principal est de transformer des données brutes issues du scraping en datasets fiables, structurés et prêts pour l’analyse et l’intelligence artificielle.

🏗️ Architecture globale du projet
AVITO_PIPELINE/
│
├── app/
│   └── app.py
│
├── extract/
│   └── scraper.py
│
├── clean/
│   └── cleaner.py
│
├── staging/
│
├── warehouse/
│   ├── database_setup.py
│   ├── load_to_warehouse.py
│   └── main.py
│
├── ml/
│   ├── preprocessing.py
│   ├── features.py
│   ├── split.py
│   ├── train.py
│   ├── train_regression.py
│   ├── train_classification.py
│   ├── evaluate.py
│   ├── extract_obt.py
│   └── run_pipeline.py
│
├── models/
│
├── logs/
│
├── image/
│
├── pipeline/
│
├── docker-compose.yml
├── Dockerfile.pipeline
├── requirements.txt
├── init.sql
└── README.md
🎯 Objectifs du projet
📊 Partie Data Engineering
Scraper les annonces immobilières depuis Avito.ma
Stocker les données brutes dans une zone staging
Nettoyer et standardiser les données
Construire un Data Warehouse
Créer un schéma BI optimisé pour Power BI
Créer un schéma ML sous forme OBT (One Big Table)
Automatiser tout le pipeline avec Docker Compose
🤖 Partie Machine Learning
Extraire les données depuis le schéma ML
Préparer les données pour l’apprentissage
Construire des modèles de régression et classification
Évaluer les performances des modèles
Exporter les modèles entraînés
⚙️ Technologies utilisées
🔹 Backend & Data
Python
Pandas
NumPy
SQLAlchemy
Scikit-learn
Imbalanced-learn (SMOTE)
🔹 Scraping
Selenium
Requests
BeautifulSoup
🔹 Base de données
PostgreSQL / SQL Server
Docker Compose
🔹 Visualisation
Power BI
🔹 Machine Learning
Scikit-learn
Random Forest
Linear Regression
Logistic Regression
XGBoost (optionnel)
📥 Extraction des données

Le scraping récupère uniquement les données publiques et non personnelles des annonces immobilières.

📌 Données collectées
Titre de l’annonce
Prix
Ville
Quartier
Surface
Nombre de chambres
Nombre de salles de bain
Étage
Année de construction
Lien de l’annonce
❌ Données exclues

Aucune donnée personnelle n’est collectée :

Noms
Emails
Numéros de téléphone
Adresses exactes
Informations identifiantes
🔐 Conformité & RGPD

Le pipeline respecte les principes de conformité des données.

✅ Mesures appliquées
Minimisation des données collectées
Suppression des données sensibles
Respect des conditions d’utilisation
Limitation de la conservation des données
Sécurisation du pipeline
Journalisation des opérations (logs)
Traçabilité complète du scraping
🗂️ Couche Staging

La couche staging sert de zone temporaire pour stocker les données brutes avant transformation.

📌 Fonctionnalités
Gestion des erreurs de scraping
Gestion automatique de la pagination
Logs des requêtes
Contrôle qualité initial
Réutilisation ou nettoyage automatique
🧹 Clean Layer

Les données passent ensuite par une phase de nettoyage structurée.

✅ Traitements appliqués
Suppression des doublons
Gestion des valeurs manquantes
Correction des types de données
Standardisation des villes et quartiers
Détection des valeurs aberrantes
Validation des données

Cette étape produit un dataset fiable et cohérent.

🧠 Feature Engineering

Des variables dérivées sont créées pour améliorer l’analyse métier et les performances ML.

📌 Features créées
Prix par m²
Âge du bien immobilier
Ratios prix / surface
Variables géographiques
Variables temporelles
Interactions entre variables
Log transformation des prix
🏢 Data Warehouse

Le Data Warehouse contient deux schémas principaux.

📊 BI Schema (bi_schema)

Le schéma BI est conçu pour l’analyse décisionnelle et Power BI.

🧩 Modélisation
Star Schema
Snowflake Schema
Galaxy Schema
📌 Tables principales
Fact Tables
Fact_Annonce
Dimension Tables
Dim_Temps
Dim_Localisation
Dim_Caracteristiques
Dim_Surface
🎯 Objectif

Optimiser :

Les performances Power BI
Les requêtes analytiques
Les dashboards décisionnels
🤖 ML Schema (ml_schema)

Le schéma ML contient une OBT (One Big Table).

📌 Contenu
Toutes les features consolidées
Structure plate
Dataset prêt pour le Machine Learning
⚠️ Important

Les transformations ML ne sont PAS réalisées dans la base.

Les opérations suivantes sont effectuées après extraction :

Encoding
Scaling
Normalisation
SMOTE
Split Train/Test
🔄 Pipeline Machine Learning

Le pipeline ML suit les étapes suivantes :

Extraction OBT
      ↓
Train/Test Split
      ↓
Feature Engineering
      ↓
Encoding & Scaling
      ↓
Training
      ↓
Evaluation
      ↓
Export Models
📈 Modèle de Régression
🎯 Objectif

Prédire le prix des biens immobiliers.

📌 Étapes
Sélection des features
Entraînement du modèle
Validation croisée
Optimisation des hyperparamètres
📊 Métriques utilisées
MAE
MSE
RMSE
R² Score
🧠 Modèle de Classification
🎯 Objectif

Prédire certaines caractéristiques immobilières.

Exemples :

Type de bien
Présence d’un équipement
Catégorie de prix
📊 Métriques utilisées
Accuracy
Precision
Recall
F1-Score
ROC-AUC
📊 Analyse des résultats

Le projet inclut :

Analyse des erreurs
Importance des features
Comparaison des modèles
Détection du surapprentissage
Optimisation des performances
🔁 Automatisation du pipeline

Le pipeline complet est automatisé via Docker Compose.

⚙️ Exécution séquentielle
Scraping
   ↓
Staging
   ↓
Cleaning
   ↓
Warehouse
   ↓
ML Pipeline
✅ Fonctionnalités
Retry automatique
Logs centralisés
Réexécution automatique
Isolation des services
Reproductibilité complète
🐳 Docker Compose

Le projet utilise Docker Compose pour :

Base de données
Pipeline ETL
Automatisation
Isolation des dépendances
▶️ Lancer le projet
docker-compose up --build
🗃️ Logs & Monitoring

Tous les traitements sont tracés.

📌 Logs disponibles
Logs scraping
Logs ETL
Logs erreurs
Logs ML
Historique d’exécution
✅ Validation des données

Des contrôles sont appliqués pour garantir :

Cohérence des données
Intégrité des relations
Complétude des datasets
Qualité du Data Warehouse
Validité des features ML
📊 Power BI

Le schéma BI est connecté à Power BI afin de créer :

Dashboards interactifs
KPIs immobiliers
Analyses géographiques
Analyses temporelles
Visualisations décisionnelles
🚀 Résultat final

À la fin du projet, le pipeline permet de :

✅ Scraper automatiquement les annonces immobilières

✅ Nettoyer et standardiser les données

✅ Construire un Data Warehouse professionnel

✅ Alimenter Power BI

✅ Générer un dataset ML prêt pour l’entraînement

✅ Automatiser entièrement le workflow

✅ Produire des modèles prédictifs immobiliers