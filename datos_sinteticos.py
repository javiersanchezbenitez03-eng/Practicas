from faker import Faker
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Configuración de localización y semillas para reproducibilidad
fake = Faker('es_MX')
Faker.seed(42)
np.random.seed(42)

# 1. Generación programática de dataset sintético (1,000 registros)
registros = []
for i in range(1000):
    registros.append({
        'id_cliente': i + 1,
        'nombre': fake.name(),
        'email': fake.email(),
        # ADECUACIÓN 1: Campos sintéticos adicionales
        'direccion': fake.address().replace('\n', ', '),
        'telefono': fake.phone_number(),
        'estado_civil': np.random.choice(['Soltero', 'Casado', 'Divorciado'], p=[0.5, 0.4, 0.1]),
        'ingreso_anual': round(np.random.uniform(100000, 1000000), 2),
        'churn': np.random.choice([0, 1], p=[0.8, 0.2])  # 20% tasa de abandono desbalanceada
    })

df_sintetico = pd.DataFrame(registros)

print("=== MUESTRA DEL DATASET SINTÉTICO GENERADO ===")
print(df_sintetico[['id_cliente', 'nombre', 'estado_civil', 'ingreso_anual', 'churn']].head())

# 2. ADECUACIÓN 2: Codificación de variables categóricas (One-Hot Encoding con pd.get_dummies)
df_encoded = pd.get_dummies(df_sintetico, columns=['estado_civil'], drop_first=False)

# 3. Selección de Datos Objetivo (Target) y Características (Features)
# Excluimos identificadores y datos de texto libre sensibles
X = df_encoded.drop(columns=['id_cliente', 'nombre', 'email', 'direccion', 'telefono', 'churn'])
y = df_encoded['churn']

# 4. Partición Estratificada (Train 80%, Test 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# 5. Análisis de proporciones para reporte
print("\n=== ANÁLISIS DE PROPORCIONES DE CHURN ===")
print(f"Dataset Completo - Proporción Churn (Clase 1): {y.mean():.4f} ({y.mean()*100:.2f}%)")
print(f"Train Set         - Proporción Churn (Clase 1): {y_train.mean():.4f} ({y_train.mean()*100:.2f}%)")
print(f"Test Set          - Proporción Churn (Clase 1): {y_test.mean():.4f} ({y_test.mean()*100:.2f}%)")

print(f"\nDimensiones Train Set: {X_train.shape}")
print(f"Dimensiones Test Set: {X_test.shape}")
