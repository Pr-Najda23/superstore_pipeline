import pandas as pd
import os
import re

def clean_layer_pipeline():
    # 1. تحديد المسارات (Paths)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "..", "avito_data_clean.csv")
    output_file = os.path.join(base_dir, "..", "staging", "avito_final_refined.csv")

    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        return

    # 2. Chargement des données
    df = pd.read_csv(input_file)
    print(f"🚀 Processing {len(df)} rows...")

    # 3. Suppression des doublons (بناءً على الرابط link)
    df.drop_duplicates(subset=['link'], keep='first', inplace=True)

    # 4. Correction des types (Price)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # 5. Standardisation (City)
    # كنستخرجو المدينة اللي كتجي مباشرة مورا كلمة 'dans '
    def extract_city(location):
        match = re.search(r'dans\s+([^,]+)', str(location))
        return match.group(1).strip() if match else "Inconnu"

    df['city'] = df['location'].apply(extract_city)

    # 6. Extraction de Surface (بدقة عالية)
    def extract_surface(surface_str):
        if pd.isna(surface_str): return None
        nums = re.findall(r'\d+', str(surface_str))
        return int(nums[0]) if nums else None

    df['surface_m2'] = df['surface'].apply(extract_surface)

    # 7. Gestion des valeurs manquantes (Imputation)
    # السطور اللي مافيهمش المساحة (بحال 25 و 28 فالتصويرة) غنعطيوهم متوسط المساحة ديال ديك المدينة
    df['surface_m2'] = df.groupby('city')['surface_m2'].transform(lambda x: x.fillna(x.median()))

    # 8. Traitement des valeurs aberrantes (Outliers)
    # كنحيدو أي شقة ثمنها قل من 100,000 درهم
    df = df[df['price'] >= 100000]

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"✅ Clean Layer Applied Successfully!")
    print(f"📊 Rows after cleaning: {len(df)}")
    print(f"📍 Result saved in: staging/avito_final_refined.csv")

if __name__ == "__main__":
    clean_layer_pipeline()