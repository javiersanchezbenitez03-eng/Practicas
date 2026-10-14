import boto3
from botocore.config import Config
import pandas as pd
import json
import io

# --- CREDENCIALES DE AWS S3 (Tus credenciales activas de AWS Academy) ---
AWS_ACCESS_KEY_ID = "ASIASO2ZG7GX2VLCI7NX"
AWS_SECRET_ACCESS_KEY = "wEeiKvNSqxgTI54GVV3Zraz3XiK/C4clgQD3slEW"
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

BUCKET_NAME = 'aws-academy-datacenter-bucket-23-02-011'
REGION_NAME = 'us-west-2'

# 1. Configuración de cliente Boto3 para conexión con AWS Academy S3 (con soporte de token y región)
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
