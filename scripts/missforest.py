import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import OrdinalEncoder
from pathlib import Path

# Esto detecta automáticamente la raíz de tu proyecto basándose en la ubicación del script
BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "eventzella_schema.xlsx"

print(f"Buscando archivo en: {FILE_PATH}")

# Carga el archivo usando la ruta absoluta generada
try:
    df_original = pd.read_excel(FILE_PATH, sheet_name='EVENT')
    print("¡Conexión exitosa con el Excel!")
except FileNotFoundError:
    print("ERROR: El archivo no está en la carpeta data. Revisa la estructura.")

# 2. Crear una copia de trabajo para no afectar al original
df_working = df_original.copy()

print(f"Datos cargados: {df_working.shape[0]} filas.")
print(f"Presupuestos faltantes detectados: {df_working['budget'].isnull().sum()}")

# 3. Ingeniería de variables para mejorar la puntería del modelo
# Extraemos el mes de la fecha porque el presupuesto suele variar por temporada
df_working['event_month'] = pd.to_datetime(df_working['event_date']).dt.month

# 4. Preparación de datos para MissForest
# Seleccionamos variables que ayuden a predecir el budget (evitamos IDs y títulos)
features = ['budget', 'type', 'event_month']
df_subset = df_working[features].copy()

# Codificamos la columna 'type' (de texto a números)
encoder = OrdinalEncoder()
df_subset['type'] = encoder.fit_transform(df_subset[['type']].astype(str))

# 5. Configuración y ejecución de MissForest
print("Calculando valores faltantes (MissForest)...")
rf_imputer = IterativeImputer(
    estimator=RandomForestRegressor(n_estimators=100, random_state=42),
    max_iter=10,
    random_state=42
)

# Aplicamos la imputación solo al subset numérico
imputed_array = rf_imputer.fit_transform(df_subset)

# 6. Reintegrar el resultado al DataFrame de trabajo
# Solo actualizamos la columna 'budget' con los valores ya completados
df_working['budget'] = imputed_array[:, 0] # La columna 0 es 'budget'

# Eliminamos la columna auxiliar 'event_month' antes de exportar
df_working = df_working.drop(columns=['event_month'])

# 7. Exportar a un nuevo archivo Excel
output_name = 'event_budget_imputed.xlsx'
df_working.to_excel(output_name, index=False)

print("-" * 30)
print(f"¡Proceso finalizado con éxito!")
print(f"Archivo guardado como: {output_name}")
print(f"Nulos restantes en budget: {df_working['budget'].isnull().sum()}")