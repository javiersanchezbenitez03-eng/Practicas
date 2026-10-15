import boto3
from botocore.config import Config
import pandas as pd
import json
import io

BUCKET_NAME = 'aws-academy-datacenter-bucket-23-02-011'
REGION_NAME = 'us-west-2'

# 1. Configuración de cliente Boto3 (Boto3 leerá las credenciales automáticamente de ~/.aws/credentials)
custom_config = Config(
    region_name=REGION_NAME,
    signature_version='s3v4'
)

s3_client = boto3.client(
    's3',
    config=custom_config
)

def cargar_y_perfilar_s3(file_key, is_json=False):
    """Descarga archivos desde S3 y genera un perfilamiento básico de tipos de datos."""
    print(f"\n=== Procesando objeto S3: {file_key} ===")
    
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    body = response['Body'].read()

    if is_json:
        data_json = json.loads(body.decode('utf-8'))
        df = pd.json_normalize(data_json)
    else:
        df = pd.read_csv(io.BytesIO(body))

    print(f"Dimensiones del dataset: {df.shape[0]} filas x {df.shape[1]} columnas")
    print("\nPerfil de Tipos de Datos e Identificación de Tipos:")
    print(df.dtypes)
    print("\nResumen de Estadísticos Descriptivos (Cuantitativos):")
    print(df.describe().T)

    return df

# Ejemplo de ejecución dentro del entorno virtual
if __name__ == "__main__":
    df_transacciones = cargar_y_perfilar_s3('raw/transacciones.csv')
    df_logs = cargar_y_perfilar_s3('raw/logs_m2m.json', is_json=True)
