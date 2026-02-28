import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from pathlib import Path
# --------------------------------------------------
# 1. Cargar archivo
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "competitor.xlsx"

df_original = pd.read_excel(FILE_PATH)
print("Excel cargado correctamente.")

df_working = df_original.copy()

# --------------------------------------------------
# 2. Limpieza de datos
# --------------------------------------------------

# Convertir starting_price a numérico (texto → NaN)
df_working['starting_price'] = pd.to_numeric(
    df_working['starting_price'],
    errors='coerce'
)

# Asegurar que columnas numéricas estén bien tipadas
numeric_columns = ['rating_stars', 'value_money', 'functionality']

for col in numeric_columns:
    df_working[col] = pd.to_numeric(df_working[col], errors='coerce')

# --------------------------------------------------
# 3. Selección de columnas para KNN
# --------------------------------------------------
features = [
    'starting_price',
    'rating_stars',
    'value_money',
    'functionality'
]

df_subset = df_working[features].copy()

# --------------------------------------------------
# 4. Escalado (MUY importante para KNN)
# --------------------------------------------------
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_subset)

# --------------------------------------------------
# 5. Imputación KNN
# --------------------------------------------------
print("Imputando starting_price con KNN...")

knn_imputer = KNNImputer(
    n_neighbors=5,
    weights="distance"
)

imputed_array = knn_imputer.fit_transform(df_scaled)

# --------------------------------------------------
# 6. Desescalar resultados
# --------------------------------------------------
df_imputed = pd.DataFrame(
    scaler.inverse_transform(imputed_array),
    columns=features
)

# --------------------------------------------------
# 7. Reintegrar SOLO starting_price
# --------------------------------------------------
df_working['starting_price'] = df_imputed['starting_price']

# --------------------------------------------------
# 8. Exportar resultado
# --------------------------------------------------
output_name = "competitor_starting_price_knn_imputed.xlsx"
df_working.to_excel(output_name, index=False)

print("-" * 40)
print("Proceso finalizado correctamente.")
print(f"Archivo guardado como: {output_name}")
