import pandas as pd
from sqlalchemy import create_engine, text
import os, logging, shutil
from dotenv import load_dotenv
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [warehouse] %(message)s")
log = logging.getLogger(__name__)
load_dotenv()

host = os.getenv("DB_HOST", "localhost")
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{host}:5432/{os.getenv('DB_NAME')}")

def load():
    df = pd.read_csv("staging/avito_final_refined.csv").dropna(subset=["city", "surface_m2", "price"])
    log.info(f" {len(df)} lignes")

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE bi_schema.fact_annonce, bi_schema.dim_caracteristiques, bi_schema.dim_localisation, ml_schema.obt_avito_dataset RESTART IDENTITY CASCADE"))

        df[["city"]].drop_duplicates().to_sql("dim_localisation", conn, schema="bi_schema", if_exists="append", index=False)
        loc = pd.read_sql("SELECT loc_id, city FROM bi_schema.dim_localisation", conn)

        df[["surface_m2", "segment"]].drop_duplicates().to_sql("dim_caracteristiques", conn, schema="bi_schema", if_exists="append", index=False)
        carac = pd.read_sql("SELECT carac_id, surface_m2, segment FROM bi_schema.dim_caracteristiques", conn)

        df.merge(loc, on="city").merge(carac, on=["surface_m2", "segment"])[["loc_id", "carac_id", "price", "price_per_m2"]].to_sql("fact_annonce", conn, schema="bi_schema", if_exists="append", index=False)
        df.rename(columns={"segment": "market_segment"})[["city", "surface_m2", "market_segment", "price_per_m2", "price"]].to_sql("obt_avito_dataset", conn, schema="ml_schema", if_exists="append", index=False)

        # Validation
        for t in ["bi_schema.fact_annonce", "bi_schema.dim_localisation", "bi_schema.dim_caracteristiques", "ml_schema.obt_avito_dataset"]:
            log.info(f"   {t}: {conn.execute(text(f'SELECT COUNT(*) FROM {t}')).scalar()} lignes")

        orphans = conn.execute(text("SELECT COUNT(*) FROM bi_schema.fact_annonce f LEFT JOIN bi_schema.dim_localisation l ON f.loc_id=l.loc_id WHERE l.loc_id IS NULL")).scalar()
        log.info(f"   {'✅' if orphans==0 else '❌'} Orphelins: {orphans}")

    # Archive staging
    os.makedirs("staging/archive", exist_ok=True)
    shutil.copy("staging/avito_final_refined.csv", f"staging/archive/avito_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    log.info(" Done!")

if __name__ == "__main__":
    load()