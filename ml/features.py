import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def generer_caracteristiques_avancees(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series):
    """
    Ligne par ligne : Calcule et ajoute des caractéristiques avancées (Ratios géographiques,
    Interactions et Transformations) sur les ensembles Train et Test.
    """
    log.info("Démarrage du Feature Engineering avancé et enrichi...")

    # نأخذ نسخة من البيانات باش ما نخربوش الداتا الأصلية
    X_train_enrichi = X_train.copy()
    X_test_enrichi = X_test.copy()

    # --- 1. CALCUL DES RATIOS ET INDICATEURS GÉOGRAPHIQUES ENRICHIS ---
    log.info("Calcul des indicateurs géographiques enrichis (Ratio Prix/Surface moyen par ville)...")
    
    # نجمعو مؤقتاً X_train مع y_train باش نحسبو المؤشرات بلا ما نقيسو الـ Test (لعدم وقوع Leakage)
    df_temporaire = X_train.copy()
    df_temporaire['prix_reel'] = y_train
    
    # حساب سعر المتر المربع لكل عقار فـ الـ Train
    df_temporaire['ratio_prix_surface'] = df_temporaire['prix_reel'] / df_temporaire['surface_m2']
    
    # دابا غانجبدو العمود الأصلي ديال المدينة قبل الـ OneHotEncoding
    # حيت الـ DataFrame الحالي فيه أعمدة بحال city_Casablanca، غانرجعو نجبدو اسم المدينة
    # لتبسيط العملية: غانحسبو المعدل بناءً على الأعمدة الثنائية المتوفرة
    
    colonnes_villes = [col for col in X_train.columns if col.startswith('city_')]
    
    # نجهزو أعمدة جديدة فـ الـ Train والـ Test غانعمروهم بـ 0 كقيمة أولية
    X_train_enrichi['avg_prix_m2_ville'] = 0.0
    X_test_enrichi['avg_prix_m2_ville'] = 0.0
    
    for col_ville in colonnes_villes:
        # نأخذ العقارات اللي كاينين ف هاد المدينة فـ الـ Train Set
        villas_dans_ville = df_temporaire[df_temporaire[col_ville] == 1]
        
        if len(villas_dans_ville) > 0:
            # نحسبو متوسط سعر المتر المربع ف هاد المدينة فـ الـ Train
            moyenne_prix_m2 = villas_dans_ville['ratio_prix_surface'].mean()
        else:
            moyenne_prix_m2 = df_temporaire['ratio_prix_surface'].mean() # قيمة احتياطية
            
        # نوزعو هاد المتوسط على الـ Train والـ Test فاش كتكون المدينة متطابقة
        X_train_enrichi.loc[X_train_enrichi[col_ville] == 1, 'avg_prix_m2_ville'] = moyenne_prix_m2
        X_test_enrichi.loc[X_test_enrichi[col_ville] == 1, 'avg_prix_m2_ville'] = moyenne_prix_m2

    # --- 2. INTERACTION ENTRE VARIABLES (Surface × Grandes Villes) ---
    log.info("Création des variables d'interaction (Surface × Villes Principales)...")
    
    # تفاعل المساحة مع الدار البيضاء
    if 'city_Casablanca' in X_train_enrichi.columns:
        X_train_enrichi['interaction_surface_casa'] = X_train_enrichi['surface_m2'] * X_train_enrichi['city_Casablanca']
        X_test_enrichi['interaction_surface_casa'] = X_test_enrichi['surface_m2'] * X_test_enrichi['city_Casablanca']
        
    # تفاعل المساحة مع مراكش
    if 'city_Marrakech' in X_train_enrichi.columns:
        X_train_enrichi['interaction_surface_marrakech'] = X_train_enrichi['surface_m2'] * X_train_enrichi['city_Marrakech']
        X_test_enrichi['interaction_surface_marrakech'] = X_test_enrichi['surface_m2'] * X_test_enrichi['city_Marrakech']

    # --- 3. LOG TRANSFORMATION DES PRIX (VARIABLE CIBLE) ---
    log.info("Application de la transformation logarithmique sur la variable cible (Prix)...")
    y_train_log = np.log1p(y_train)
    y_test_log = np.log1p(y_test)

    log.info(f"Feature Engineering terminé ! Nombre de caractéristiques finales : {X_train_enrichi.shape[1]}")
    return X_train_enrichi, X_test_enrichi, y_train_log, y_test_log