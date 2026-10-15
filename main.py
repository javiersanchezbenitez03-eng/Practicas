import io
import boto3
import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError

def profile_s3_datasets():
    # Boto3 leerá automáticamente las credenciales desde ~/.aws/credentials
    s3_client = boto3.client('s3')
    
    bucket_name = 'aws-academy-datacenter-bucket-23-02-011'
    csv_key = 'raw/transacciones.csv'
    json_key = 'raw/logs_m2m.json'

    print("--- INICIANDO PROCESO DE INGESTA Y PROFILING EN SÚPER MEMORIA (io.BytesIO) ---")

    try:
        # 1. Procesamiento de CSV desde S3 en Memoria
        print(f"\n[1/2] Descargando y analizando CSV: {csv_key}...")
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=csv_key)
        csv_content = csv_obj['Body'].read()
        
        # Ingesta en memoria usando io.BytesIO
        df_csv = pd.read_csv(io.BytesIO(csv_content))
        
        print("--- Resumen Estadístico (CSV) ---")
        print(df_csv.info())
        print(df_csv.describe())

        # 2. Procesamiento de JSON desde S3 en Memoria
        print(f"\n[2/2] Descargando y analizando JSON: {json_key}...")
        json_obj = s3_client.get_object(Bucket=bucket_name, Key=json_key)
        json_content = json_obj['Body'].read()
        
        # Ingesta en memoria usando io.BytesIO con pandas
        df_json = pd.read_json(io.BytesIO(json_content))
        
        print("--- Resumen Estadístico (JSON) ---")
        print(df_json.info())
        print(df_json.head())

    except NoCredentialsError:
        print("[ERROR CRÍTICO] No se encontraron credenciales de AWS configuradas en el entorno.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"[ERROR] El archivo o bucket especificado no existe en S3.")
        else:
            print(f"[ERROR DE AWS]: {e}")
    except Exception as e:
        print(f"[ERROR INESPERADO]: {str(e)}")

if __name__ == "__main__":
    profile_s3_datasets()
