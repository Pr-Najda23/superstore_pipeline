-- =========================
-- SCHEMAS
-- =========================
CREATE SCHEMA IF NOT EXISTS bi_schema;
CREATE SCHEMA IF NOT EXISTS ml_schema;

-- =========================
-- BI - FACT TABLE
-- =========================
CREATE TABLE IF NOT EXISTS bi_schema.fact_annonce (
    id SERIAL PRIMARY KEY,
    link TEXT UNIQUE,
    price FLOAT,
    surface_m2 FLOAT,
    city TEXT,
    segment TEXT,
    price_per_m2 FLOAT
);

-- =========================
-- BI - DIM LOCATION
-- =========================
CREATE TABLE IF NOT EXISTS bi_schema.dim_localisation (
    city TEXT PRIMARY KEY
);

-- =========================
-- BI - DIM CARACTERISTIQUES
-- =========================
CREATE TABLE IF NOT EXISTS bi_schema.dim_caracteristiques (
    id SERIAL PRIMARY KEY,
    surface_m2 FLOAT,
    segment TEXT
);

-- =========================
-- ML - OBT TABLE (ONE BIG TABLE)
-- =========================
CREATE TABLE IF NOT EXISTS ml_schema.obt_avito_dataset (
    id SERIAL PRIMARY KEY,
    price FLOAT,
    surface_m2 FLOAT,
    city TEXT,
    segment TEXT,
    price_per_m2 FLOAT
);