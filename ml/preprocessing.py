import logging
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# إعداد السجلات (Logs) باش نتبعو تنفيذ الكود سطر بسطر بالفرنسية
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def creer_pipeline_transformation(variables_categorielles, variables_numeriques):
    """
    سطر بسطر: بناء الـ Pipeline اللي كايعالج القيم الناقصة، والـ Encoding والـ Scaling
    """
    log.info("Construction du pipeline de traitement des données...")

    # 1. معالجة الأرقام (المساحة): تعويض القيم الناقصة بالـ Median + تطبيق الـ StandardScaler
    pipeline_numerique = Pipeline(steps=[
        ('imputeur_num', SimpleImputer(strategy='median')),  # إذا كانت شي مساحة خاوية كايعمرها بالوسيط
        ('standardisation', StandardScaler())                # كايخلي المعدل = 0 والـ Écart-type = 1
    ])

    # 2. معالجة الكلمات (المدينة والـ Segment): تعويض الناقص بـ الكلمة الأكثر تكراراً + OneHotEncoder
    pipeline_categoriel = Pipeline(steps=[
        ('imputeur_cat', SimpleImputer(strategy='most_frequent')), # إذا كانت شي خانة خاوية
        ('encodage_unique', OneHotEncoder(handle_unknown='ignore', sparse_output=False)) # كايحول الكلمات لأعمدة (0 و 1)
    ])

    # 3. تجميع هاد الجوج Pipelines فـ محول واحد (ColumnTransformer) وكل واحد كيمشي للعمود ديالو
    transformateur_global = ColumnTransformer(
        transformers=[
            ('bloc_num', pipeline_numerique, variables_numeriques),
            ('bloc_cat', pipeline_categoriel, variables_categorielles)
        ]
    )
    
    return transformateur_global


def preparer_et_transformer_donnees(X_entrainement: pd.DataFrame, X_test: pd.DataFrame):
    """
    سطر بسطر: تطبيق التحويلات بلا ما يوقع Data Leakage (تحويلات ما بعد قاعدة البيانات)
    """
    log.info("Début de la préparation des caractéristiques immobilières...")

    # غانحددو الأعمدة اللي غانخدمو بيها (قصينا id و price_per_m2 حيت هاد الأخير نتيجة مباشرة للثمن)
    variables_categorielles = ['city', 'market_segment']
    variables_numeriques = ['surface_m2']

    # عيطنا على الدالة اللي صاوبنا الفوق باش تعطينا الـ Pipeline واجد
    transformateur = creer_pipeline_transformation(variables_categorielles, variables_numeriques)

    # هنا كانديرو الحساب والتحويل (Fit & Transform) على الـ Train بوحدو
    log.info("Application du Fit_Transform sur l'ensemble d'entraînement...")
    X_train_transforme = transformateur.fit_transform(X_entrainement[variables_categorielles + variables_numeriques])

    # هنا كانديرو غير التحويل (Transform) فقط على الـ Test بلا ما نعاودو نحسبو المعدل أو الـ Median
    log.info("Application du Transform sur l'ensemble de test...")
    X_test_transforme = transformateur.transform(X_test[variables_categorielles + variables_numeriques])

    # كاجبدو الأسماء الجديدة ديال الأعمدة اللي تخلقت مورا الـ OneHotEncoder آوتوماتيكياً (مثلا city_Casablanca)
    encodeur_catégoriel = transformateur.named_transformers_['bloc_cat'].named_steps['encodage_unique']
    noms_colonnes_cat = list(encodeur_catégoriel.get_feature_names_out(variables_categorielles))
    
    # نجمعو أسماء الأعمدة كاملة: الرقمية + اللي تدار ليها Encoding
    toutes_les_colonnes_finales = variables_numeriques + noms_colonnes_cat

    # نرجعو النتائج على شكل DataFrames نقية باش نخدمو بيها فـ المراحل الجاية
    X_train_final = pd.DataFrame(X_train_transforme, columns=toutes_les_colonnes_finales, index=X_entrainement.index)
    X_test_final = pd.DataFrame(X_test_transforme, columns=toutes_les_colonnes_finales, index=X_test.index)

    log.info(f"Transformation terminée avec succès ! Nombre total de caractéristiques : {len(toutes_les_colonnes_finales)}")
    
    return X_train_final, X_test_final, transformateur