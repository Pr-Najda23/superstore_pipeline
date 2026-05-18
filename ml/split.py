import logging
import pandas as pd
from sklearn.model_selection import train_test_split

# Configuration des logs en français
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def séparer_jeu_données(df: pd.DataFrame, colonne_cible: str = "price", taille_test: float = 0.2, état_aléatoire: int = 42):
    """
    Sépare le jeu de données en sous-ensembles d'entraînement (Train) et de test (Test).
    """
    log.info("Démarrage de la séparation des données (Train/Test Split)...")
    
    # Vérification de la présence de la colonne cible (le prix)
    if colonne_cible not in df.columns:
        raise KeyError(f"La colonne cible '{colonne_cible}' est introuvable dans le DataFrame.")
    
    # Séparation des variables prédictives (X) et de la cible (y)
    X = df.drop(columns=[colonne_cible])
    y = df[colonne_cible]
    
    # Division des données (80% pour l'entraînement, 20% pour le test)
    X_entrainement, X_test, y_entrainement, y_test = train_test_split(
        X, y, test_size=taille_test, random_state=état_aléatoire
    )
    
    log.info("Séparation des données effectuée avec succès !")
    log.info(f"Dimensions Entraînement (X) : {X_entrainement.shape} | Dimensions Test (X) : {X_test.shape}")
    
    return X_entrainement, X_test, y_entrainement, y_test