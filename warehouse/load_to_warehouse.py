import os
import pandas as pd
import shutil
from datetime import datetime
from sqlalchemy import text


def load(engine, log):

    file_path = "../staging/avito_final_refined.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV not found: {file_path}")

    df = pd.read_csv(file_path)

    df["city"] = df["city"].astype(str).str.strip().str.lower()
    df["segment"] = df["segment"].astype(str).str.strip().str.lower()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["surface_m2"] = pd.to_numeric(df["surface_m2"], errors="coerce")

    if "surface" in df.columns:
        df["surface_m2"] = df["surface_m2"].fillna(pd.to_numeric(df["surface"], errors="coerce"))

    df["surface_m2"] = df["surface_m2"].round(2)
    df["price_per_m2"] = df["price"] / df["surface_m2"]
    df = df.dropna(subset=["city", "surface_m2", "price"])

    log.info(f"DATA AFTER CLEANING: {df.shape}")
    if df.empty:
        log.warning("No data after cleaning")
        return

    with engine.begin() as conn:

        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bi_schema"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS ml_schema"))

        conn.execute(text("""
            TRUNCATE bi_schema.fact_annonce,
                     bi_schema.dim_caracteristiques,
                     bi_schema.dim_localisation,
                     ml_schema.obt_avito_dataset
            RESTART IDENTITY CASCADE
        """))

        dim_loc = df[["city"]].drop_duplicates()
        for _, row in dim_loc.iterrows():
            conn.execute(
                text("INSERT INTO bi_schema.dim_localisation (city) VALUES (:city)"),
                {"city": row["city"]}
            )

        loc = pd.read_sql("SELECT loc_id, city FROM bi_schema.dim_localisation", conn)
        loc["city"] = loc["city"].str.strip().str.lower()

        dim_carac = df[["surface_m2", "segment"]].drop_duplicates()
        for _, row in dim_carac.iterrows():
            conn.execute(
                text("INSERT INTO bi_schema.dim_caracteristiques (surface_m2, segment) VALUES (:surface_m2, :segment)"),
                {"surface_m2": row["surface_m2"], "segment": row["segment"]}
            )

        carac = pd.read_sql("SELECT carac_id, surface_m2, segment FROM bi_schema.dim_caracteristiques", conn)
        carac["segment"] = carac["segment"].str.strip().str.lower()
        carac["surface_m2"] = carac["surface_m2"].round(2)

        fact = df.merge(loc, on="city", how="left")
        fact = fact.merge(carac, on=["surface_m2", "segment"], how="left")
        fact = fact.dropna(subset=["loc_id", "carac_id"])

        log.info(f"FACT SHAPE: {fact.shape}")

        for _, row in fact.iterrows():
            conn.execute(
                text("INSERT INTO bi_schema.fact_annonce (loc_id, carac_id, price, price_per_m2) VALUES (:loc_id, :carac_id, :price, :price_per_m2)"),
                {"loc_id": int(row["loc_id"]), "carac_id": int(row["carac_id"]), "price": row["price"], "price_per_m2": row["price_per_m2"]}
            )

        ml_df = df.rename(columns={"segment": "market_segment"})[
            ["city", "surface_m2", "market_segment", "price_per_m2", "price"]
        ]
        ml_df.to_sql("obt_avito_dataset", conn, schema="ml_schema", if_exists="append", index=False)

        for t in ["bi_schema.fact_annonce", "bi_schema.dim_localisation", "bi_schema.dim_caracteristiques", "ml_schema.obt_avito_dataset"]:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
            log.info(f"{t}: {count} rows")

    archive_dir = "../staging/archive"
    os.makedirs(archive_dir, exist_ok=True)
    shutil.copy(file_path, f"{archive_dir}/avito_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    log.info("LOAD DONE SUCCESSFULLY")
