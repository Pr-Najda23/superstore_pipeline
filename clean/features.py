import pandas as pd
import os

# 1. Paths
input_file = r"C:\Users\user\Desktop\avito_pipeline\staging\avito_final_refined.csv"
output_file = r"C:\Users\user\Desktop\avito_pipeline\staging\avito_analytics_ready.csv"

df = pd.read_csv(input_file)

# 2. Prix par m²
df['price_per_m2'] = (df['price'] / df['surface_m2']).round(2)

# 3. Market Segment (Luxury vs Eco)
def get_segment(row):
    if row['price'] > 2000000: return 'Luxe'
    if row['price'] < 600000: return 'Economique'
    return 'Moyen'

df['segment'] = df.apply(get_segment, axis=1)

# 4. Standard City Names
df['city'] = df['city'].str.capitalize()

# 5. Save
df.to_csv(output_file, index=False)
print(f"✅ Features Added! Saved to: {output_file}")