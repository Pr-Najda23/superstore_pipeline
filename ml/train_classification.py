import logging
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def entrainer_et_evaluer_classification(X_train: pd.DataFrame, X_test: pd.DataFrame, df_obt_original: pd.DataFrame):
    """
    Ligne par ligne : Crée la cible, applique SMOTE, entraîne plusieurs modèles (Logistic Regression 
    et Random Forest) et calcule l'ensemble des métriques demandées (Accuracy, Precision, Recall, F1, ROC-AUC).
    """
    log.info("Démarrage du module de Classification des caractéristiques immobilières...")

    # 1. CRÉATION DE LA VARIABLE CIBLE BINAIRE (Ex: Le bien est-il dans le segment 'Luxe' ?)
    # On utilise l'index pour s'aligner parfaitement avec le Train et le Test issus du Split
    y_train_cible = (df_obt_original.loc[X_train.index, 'market_segment'] == 'Luxe').astype(int)
    y_test_cible = (df_obt_original.loc[X_test.index, 'market_segment'] == 'Luxe').astype(int)

    # Pour éviter le Target Leakage, on supprime les colonnes de segment issues du OneHotEncoder dans X
    colonnes_segment = [col for col in X_train.columns if col.startswith('market_segment_')]
    X_train_cls = X_train.drop(columns=colonnes_segment)
    X_test_cls = X_test.drop(columns=colonnes_segment)

    # 2. GESTION DU DÉSÉQUILIBRE DES CLASSES (Traitement SMOTE)
    log.info(f"Distribution de la cible avant SMOTE : Class 0: {str(sum(y_train_cible == 0))}, Class 1 (Luxe): {str(sum(y_train_cible == 1))}")
    
    # Application de SMOTE pour équilibrer le jeu d'entraînement
    log.info("Application de SMOTE sur l'ensemble d'entraînement...")
    smote = SMOTE(random_state=42, k_neighbors=2)
    X_train_equilibre, y_train_equilibre = smote.fit_resample(X_train_cls, y_train_cible)
    
    log.info(f"Distribution après SMOTE : Class 0: {str(sum(y_train_equilibre == 0))}, Class 1: {str(sum(y_train_equilibre == 1))}")

    # 3. ENTRAÎNEMENT DE PLUSIEURS MODÈLES
    modeles = {
        "Régression Logistique": LogisticRegression(max_iter=1000, random_state=42),
        "Forêt Aléatoire (Random Forest)": RandomForestClassifier(random_state=42, n_estimators=100)
    }

    resultats_globaux = {}

    for nom_modele, modele in modeles.items():
        log.info(f"Entraînement du modèle : {nom_modele}...")
        modele.fit(X_train_equilibre, y_train_equilibre)

        # Prédictions des classes et des probabilités (nécessaires pour le ROC-AUC)
        y_pred = modele.predict(X_test_cls)
        y_prob = modele.predict_proba(X_test_cls)[:, 1]

        # 4. CALCUL DES MÉTRIQUES DEMANDÉES
        accuracy = accuracy_score(y_test_cible, y_pred)
        precision = precision_score(y_test_cible, y_pred, zero_division=0)
        recall = recall_score(y_test_cible, y_pred, zero_division=0)
        f1 = f1_score(y_test_cible, y_pred, zero_division=0)
        
        # Gestion du cas où une seule classe est présente dans le jeu de test pour le calcul ROC-AUC
        try:
            roc_auc = roc_auc_score(y_test_cible, y_prob)
        except ValueError:
            roc_auc = np.nan

        resultats_globaux[nom_modele] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'rapport': classification_report(y_test_cible, y_pred, zero_division=0)
        }
        log.info(f"Évaluation de {nom_modele} terminée.")

    return resultats_globaux