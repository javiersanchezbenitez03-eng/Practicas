import boto3
from botocore.config import Config
import pandas as pd
import numpy as np

# Configuración general (sin credenciales hardcodeadas)
BUCKET_NAME = "aws-academy-datacenter-bucket-23-02-011"
REGION_NAME = "us-west-2"

def generar_y_subir():
    try:
        # Configuramos boto3 para que use el entorno o las credenciales por defecto
        custom_config = Config(
            region_name=REGION_NAME,
            signature_version='s3v4'
        )
        
        # Al no pasar llaves ni tokens explícitos, boto3 los busca automáticamente en el entorno
        s3_client = boto3.client(
            's3',
            config=custom_config
        )
        
        np.random.seed(42)
        data = {
            'id_transaccion': range(1, 501),
            'monto': np.random.uniform(10.0, 5000.0, 500),
            'cliente_id': np.random.randint(100, 200, 500)
        }
        df = pd.DataFrame(data)
        archivo_local = 'transacciones.csv'
        df.to_csv(archivo_local, index=False)
        print(f"Archivo local '{archivo_local}' generado exitosamente.")
        
        ruta_s3 = "raw/transacciones.csv"
        print(f"Subiendo a s3://{BUCKET_NAME}/{ruta_s3}...")
        
        s3_client.upload_file(archivo_local, BUCKET_NAME, ruta_s3)
        print("¡Archivo subido exitosamente a S3!")
        
    except Exception as e:
        print(f"Error al subir el archivo a S3: {e}")

if __name__ == "__main__":
    generar_y_subir()
