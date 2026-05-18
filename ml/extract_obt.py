import os
import logging
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Charger les variables d'environnement (.env)
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def get_warehouse_engine():
    """
    Crée le moteur SQLAlchemy en utilisant les configurations exactes du pipeline.
    """
    # Récupération des variables avec le port 5434 spécifié dans ton main.py
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME')
    db_port = "5434" 

    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_string)
    return engine

def extract_obt_data():
    """
    Se connecte à ml_schema et extrait la table OBT (obt_avito_dataset).
    """
    engine = get_warehouse_engine()
    
    # Sélectionner toutes les features de la table OBT
    query = "SELECT * FROM ml_schema.obt_avito_dataset;"
    
    try:
        log.info("Connexion au Data Warehouse et extraction de la table OBT...")
        
        # Charger les données directement dans un DataFrame Pandas
        df = pd.read_sql_query(query, con=engine)
        
        log.info(f"Extraction réussie ! Nombre de lignes récupérées : {df.shape[0]}, Nombre de colonnes : {df.shape[1]}")
        return df
        
    except Exception as e:
        log.error(f"Erreur critique lors de l'extraction de l'OBT : {str(e)}")
        raise e

if __name__ == "__main__":
    # Test unitaire du script d'extraction
    try:
        df_obt = extract_obt_data()
        print("\n--- Aperçu des données OBT extraites ---")
        print(df_obt.head())
    except Exception:
        print("\n[Erreur] Impossible de lancer l'extraction. Vérifie que le conteneur/la DB tourne sur le port 5434.")