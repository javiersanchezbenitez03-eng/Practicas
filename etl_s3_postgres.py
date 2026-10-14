import io
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import boto3
from botocore.config import Config
import psycopg2  # Biblioteca para conectar a PostgreSQL

# --- CREDENCIALES DE AWS S3 (Actualizadas) ---
AWS_ACCESS_KEY_ID = "ASIASO2ZG7GX2VLCI7NX"
AWS_SECRET_ACCESS_KEY = "wEeiKvNSqxgTI54GVV3Zraz3XiK/C4clgQD3slEW"

# Token dividido para que no genere errores de sintaxis
AWS_SESSION_TOKEN = (
    "IQoJb3JpZ2luX2VjEPP//////////wEaCXVzLXdlc3QtMiJGMEQCID3Iqxxlue4trj7N"
    "gUD/HhdNn4go1IyI1Zrm7YX2DqtsAiBIs6+5HpMvL0lE0FzujO0sB7EUSe8eAFoxs1Ee"
    "pEg5ACqpAgi8//////////8BEAEaDDE2OTMwMTQ0MDk0MyIMkIQHgMTwLueXM97lKv0B"
    "Zjfac3ScVP5EQv6dBpSrR326w5UJe9hcjx6+v3H32j5ft7ArIY8rU7TWXBtpnsrl8EOD"
    "NuLU2xa8Tso2SOohb7Yproo/Qa9sSuNEupsi6i7+8oFavHyX11bO1GJyhUAteeeigWaHb"
    "iaHaVrfrHU+5at+PCro6UpjUJVYmE7DPcHIRLUwmRuf/SvEXubU3jw3CCWYGdEiN2kqK"
    "k88Sm6nyP3dpbDkfom02BHEgngI/LoYzhbUichQrcXlgF9VqENRwcn2xxd5QYJ9R+Yt5C"
    "vcVE0mBdIF0HgJgsV4KdFpgo4gVkAIuTZpuBq/oa/DH9wm5xQQGxrMVgLErAOaMzDdmL/"
    "WBjqeAeVzx1RSl6DFnKPkiyoyIN7CmuNfvXIq9/nq7Rpwy6o9kOt+PIKoM6NZNbALLa3+"
    "EMKjDXZRPXqKAoIsLz0J7PRWgmssnJx+AWefg7dKHBcUbPOx713adWah4QrPMNqzI1Hs"
    "uBRsBI+HfI0SB/KAWM9fOn8PuBrLqhGROaasE/mIiZXyhm84y6LCqVNoZy+phw9tlpjzf"
    "QsBJOAuweC2"
)

BUCKET_NAME = "aws-academy-datacenter-bucket-23-02-011"
REGION_NAME = "us-west-2"  # Región compatible con el token de sesión de AWS Academy

# --- CONFIGURACIÓN DE POSTGRESQL ---
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"         # Usamos la base de datos por defecto 'postgres'
DB_USER = "tu_usuario"       # El usuario que ya tienes creado
DB_PASSWORD = "123456"       # La contraseña que acabamos de asignarle


def pipeline_etl_completo():
    print("=== 1. FASE DE EXTRACCIÓN (Extract) ===")
    raw_data = {
        'cliente': ['A', 'B', 'C', 'D'],
        'edad': [20, 40, 60, 30],
        'monto_compras': [1200.0, 50000.0, 30000.0, 15000.0]
    }
    df_raw = pd.DataFrame(raw_data)
    print(df_raw)

    print("\n=== 2. FASE DE TRANSFORMACIÓN (Transform) ===")
    # Generalización
    df_raw['categoria_edad'] = pd.cut(
        df_raw['edad'], 
        bins=[0, 25, 50, 100], 
        labels=['Joven', 'Adulto', 'Senior']
    )
    
    # Normalización Min-Max de monto_compras
    scaler = MinMaxScaler()
    df_raw['monto_normalizado'] = scaler.fit_transform(df_raw[['monto_compras']])
    
    # Feature Engineering (Construcción)
    df_raw['score_promocional'] = df_raw['monto_normalizado'] * 100
    
    print("Dataset Transformado:")
    print(df_raw)

    print("\n=== 3. FASE DE CARGA (Load - AWS S3 & PostgreSQL) ===")
    
    # A. Carga hacia AWS S3 en formato Parquet
    try:
        custom_config = Config(
            region_name=REGION_NAME,
            signature_version='s3v4'
        )
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            config=custom_config
        )

        buffer = io.BytesIO()
        df_raw.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        s3_client.put_object(
            Bucket=BUCKET_NAME, 
            Key='processed/etl_output.parquet', 
            Body=buffer.getvalue()
        )
        print("-> Éxito: Archivo Parquet comprimido cargado correctamente en la zona 'processed' de S3.")
    except Exception as e:
        print(f"-> Error al conectar o subir a S3: {e}")

    # B. Carga / Inserción hacia PostgreSQL
    try:
        print("Conectando a PostgreSQL...")
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()

        # Crear tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes_procesados (
                cliente VARCHAR(10),
                edad INT,
                monto_compras FLOAT,
                categoria_edad VARCHAR(20),
                monto_normalizado FLOAT,
                score_promocional FLOAT
            );
        """)

        # Insertar registros fila por fila desde el DataFrame transformado
        for index, row in df_raw.iterrows():
            cursor.execute("""
                INSERT INTO clientes_procesados (cliente, edad, monto_compras, categoria_edad, monto_normalizado, score_promocional)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(row['cliente']),
                int(row['edad']),
                float(row['monto_compras']),
                str(row['categoria_edad']),
                float(row['monto_normalizado']),
                float(row['score_promocional'])
            ))

        connection.commit()
        cursor.close()
        connection.close()
        print("-> Éxito: Datos insertados correctamente en la base de datos PostgreSQL.")

    except Exception as e:
        print(f"-> Error al conectar o insertar en PostgreSQL: {e}")

if __name__ == "__main__":
    pipeline_etl_completo()
