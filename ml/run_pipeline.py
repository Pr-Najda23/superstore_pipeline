import os
import logging
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import joblib

# 1. استدعاء الـ Modules اللي صاوبتي بالظبط وبنفس الأسماء
from ml.extract_obt import extract_obt_data
from ml.split import séparer_jeu_données
from ml.preprocessing import preparer_et_transformer_donnees
from ml.features import generer_caracteristiques_avancees
from ml.train_regression import entrainer_et_evaluer_regression
from ml.train_classification import entrainer_et_evaluer_classification

# إعداد السجلات (Logs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# تحميل متغيرات البيئة بشكل عادي (دابا VS Code مغطيها)
load_dotenv()

def run_pipeline():
    log.info("=== 🧠 DÉMARRAGE DU PIPELINE ML INTÉGRAL (RÉGRESSION + CLASSIFICATION) ===")

    try:
        # الخطوة 1: الاستخراج النقي باستعمال extract_obt.py ديالك
        df_obt = extract_obt_data()
        log.info(f"✅ Étape 1 Réussie. Taille initiale de la table OBT: {df_obt.shape}")

        # الخطوة 2: تقسيم البيانات (Split) باستعمال split.py ديالك
        X_train, X_test, y_train, y_test = séparer_jeu_données(df_obt, colonne_cible="price", taille_test=0.2, état_aléatoire=42)

        # الخطوة 3: المعالجة والتحويل (Preprocessing) باستعمال preprocessing.py ديالك
        X_train_trans, X_test_trans, transformateur = preparer_et_transformer_donnees(X_train, X_test)

        # الخطوة 4: هندسة الميزات المتقدمة والـ Log transformation باستعمال features.py ديالك
        X_train_feat, X_test_feat, y_train_log, y_test_log = generer_caracteristiques_avancees(
            X_train_trans, X_test_trans, y_train, y_test
        )

        # الخطوة 5: تدريب وتقييم موديل الـ Régression (Ridge) باستعمال train_regression.py ديالك
        modele_reg, metriques_reg = entrainer_et_evaluer_regression(X_train_feat, X_test_feat, y_train_log, y_test_log)
        
        log.info("=== 📈 [RAPPORT] MODÈLE DE RÉGRESSION (RIDGE) ===")
        log.info(f"MAE  : {metriques_reg['mae']:.2f} MAD")
        log.info(f"RMSE : {metriques_reg['rmse']:.2f} MAD")
        log.info(f"R²   : {metriques_reg['r2']:.4f}")

        # الخطوة 6: تدريب وتقييم موديل الـ Classification (RF + SMOTE) باستعمال train_classification.py ديالك
        # كانصيفطو ليه X_train_trans (بلا الأعمدة المتقدمة والـ Log) حيت الـ Module كايتكلف بالباقي
        resultats_cls = entrainer_et_evaluer_classification(X_train_trans, X_test_trans, df_obt)
        
        log.info("=== 🧠 [RAPPORT] MODÈLE DE CLASSIFICATION (SMOTE + RF / LOG REG) ===")
        for nom_mod, res in resultats_cls.items():
            log.info(f"\n>>> Modèle: {nom_mod}")
            log.info(f"Accuracy  : {res['accuracy']:.4f}")
            log.info(f"Precision : {res['precision']:.4f}")
            log.info(f"Recall    : {res['recall']:.4f}")
            log.info(f"F1-Score  : {res['f1']:.4f}")
            log.info(f"ROC-AUC   : {res['roc_auc']:.4f}")
            log.info(f"\n<<< DETAILED REPORT >>>\n{res['rapport']}")

        # الخطوة 7: تصدير وحفظ الموديلات ف الـ dossier المخصص ليها
        os.makedirs('models', exist_ok=True)
        joblib.dump(modele_reg, 'models/ridge_regression_model.joblib')
        joblib.dump(transformateur, 'models/preprocessor_pipeline.joblib')
        log.info("✅ [EXPORT] Tous les modèles et pipelines ont été sauvegardés dans /models !")
        log.info("==========================================================================")

    except Exception as e:
        log.error(f"❌ Le pipeline s'est arrêté suite à une erreur : {str(e)}")
        raise

if __name__ == "__main__":
    run_pipeline()