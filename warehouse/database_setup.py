import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_warehouse_structure():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port="5434",
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cur = conn.cursor()

        print(f" Creating database structure in: {os.getenv('DB_NAME')}...")

        # ✅ كل command بوحدو
        commands = [
            "CREATE SCHEMA IF NOT EXISTS bi_schema;",
            "CREATE SCHEMA IF NOT EXISTS ml_schema;",

            """
            CREATE TABLE IF NOT EXISTS bi_schema.dim_localisation (
                loc_id SERIAL PRIMARY KEY,
                city VARCHAR(100)
            );
            """,

            """
            CREATE TABLE IF NOT EXISTS bi_schema.dim_caracteristiques (
                carac_id SERIAL PRIMARY KEY,
                surface_m2 FLOAT,
                segment VARCHAR(50)
            );
            """,

            """
            CREATE TABLE IF NOT EXISTS bi_schema.fact_annonce (
                annonce_id SERIAL PRIMARY KEY,
                loc_id INT REFERENCES bi_schema.dim_localisation(loc_id),
                carac_id INT REFERENCES bi_schema.dim_caracteristiques(carac_id),
                price FLOAT,
                price_per_m2 FLOAT
            );
            """,

            """
            CREATE TABLE IF NOT EXISTS ml_schema.obt_avito_dataset (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100),
                surface_m2 FLOAT,
                market_segment VARCHAR(50),
                price_per_m2 FLOAT,
                price FLOAT
            );
            """
        ]

        # 🔁 تنفيذ كل أمر بوحدو
        for cmd in commands:
            cur.execute(cmd)

        conn.commit()

        print("Success! BI and ML schemas are ready.")

    except Exception as e:
        print(f" Error: {e}")
        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    create_warehouse_structure()