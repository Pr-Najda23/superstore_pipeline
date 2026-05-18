import logging
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# إعداد السجلات لتتبع تدريب الموديل سطر بسطر
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def entrainer_et_evaluer_regression(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train_log: pd.Series, y_test_log: pd.Series):
    """
    Ligne par ligne : Entraîne un modèle de régression (Ridge) sur les données transformées,
    effectue les prédictions, inverse la transformation log, et calcule les métriques d'évaluation.
    """
    log.info("Initialisation du modèle de Régression (Régression Ridge)...")
    
    # اخترينا Ridge Regression حيت كيحمي الموديل من الـ Overfitting فاش كيكونوا الأعمدة كتار مورا الـ Encoding
    modele = Ridge(alpha=10.0)
    
    log.info("Entraînement du modèle de régression sur le jeu d'apprentissage...")
    modele.fit(X_train, y_train_log)
    
    log.info("Génération des prédictions sur les ensembles Train et Test (en échelle Log)...")
    predictions_train_log = modele.predict(X_train)
    predictions_test_log = modele.predict(X_test)
    
    # خطوة مهمة جداً: إلغاء الـ Log transformation باستعمال np.expm1 (يعني exp(x) - 1)
    # باش نرجعو الأسعار والتوقعات للقيمة الحقيقية ديالها بالدرهم (MAD) قبل ما نحسبو الأخطاء
    log.info("Inversion de la transformation logarithmique pour obtenir les prix réels en Dirhams...")
    y_train_reel = np.expm1(y_train_log)
    y_test_reel = np.expm1(y_test_log)
    
    predictions_train_reelles = np.expm1(predictions_train_log)
    predictions_test_reelles = np.expm1(predictions_test_log)
    
    # حساب مؤشرات الأداء على مجموعة الاختبار (Test Set)
    log.info("Calcul des métriques de performance sur le jeu de test...")
    mae = mean_absolute_error(y_test_reel, predictions_test_reelles)
    mse = mean_squared_error(y_test_reel, predictions_test_reelles)
    rmse = np.sqrt(mse) # جذر مربع MSE باش يعطينا قيمة الخطأ بنفس وحدة القياس (الدرهم)
    r2 = r2_score(y_test_reel, predictions_test_reelles)
    
    log.info("Évaluation du modèle de Régression terminée avec succès.")
    
    # تجميع النتائج فـ دكشنري (Dictionary) باش نخرجوهم من الدالة
    metriques = {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2
    }
    
    return modele, metriques