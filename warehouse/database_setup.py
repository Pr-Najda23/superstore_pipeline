import psycopg2
import os
from dotenv import load_dotenv

# تحميل الإعدادات من ملف .env
load_dotenv()

def create_warehouse_structure():
    conn = None
    cur = None
    try:
    
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port="5432",
            database=os.getenv("DB_NAME"), 
            user=os.getenv("DB_USER"),     
            password=os.getenv("DB_PASSWORD") 
        )
        cur = conn.cursor()

        sql_commands = """
        -- 1. creations des tables (Schemas)
        CREATE SCHEMA IF NOT EXISTS bi_schema;
        CREATE SCHEMA IF NOT EXISTS ml_schema;

        -- 2. les tables BI Schema (Star Schema)
        CREATE TABLE IF NOT EXISTS bi_schema.dim_localisation (
            loc_id SERIAL PRIMARY KEY,
            city VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS bi_schema.dim_caracteristiques (
            carac_id SERIAL PRIMARY KEY,
            surface_m2 FLOAT,
            segment VARCHAR(50)
        );

        CREATE TABLE IF NOT EXISTS bi_schema.fact_annonce (
            annonce_id SERIAL PRIMARY KEY,
            loc_id INT REFERENCES bi_schema.dim_localisation(loc_id),
            carac_id INT REFERENCES bi_schema.dim_caracteristiques(carac_id),
            price FLOAT,
            price_per_m2 FLOAT
        );

        -- 3.  les tables ML Schema (One Big Table)
        CREATE TABLE IF NOT EXISTS ml_schema.obt_avito_dataset (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            surface_m2 FLOAT,
            market_segment VARCHAR(50),
            price_per_m2 FLOAT,
            price FLOAT
        );
        """
        
        print(f" Creating database structure in: {os.getenv('DB_NAME')}...")
        cur.execute(sql_commands)
        conn.commit()
        print(f"Success! BI and ML schemas are now ready.")

    except Exception as e:
        print(f" Error during connection or execution: {e}")
        if conn:
            conn.rollback()
    
    finally:

        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_warehouse_structure()