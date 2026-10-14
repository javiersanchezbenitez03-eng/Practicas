import boto3
from botocore.config import Config
import pandas as pd
import numpy as np

AWS_ACCESS_KEY_ID = "ASIASO2ZG7GX6UDFF7QN"
AWS_SECRET_ACCESS_KEY = "CTHgzuQ5aszNo3A/+nVE+I3oLtu0boetFeLnc8W5"

# Token dividido en partes para que se mantenga limpio
AWS_SESSION_TOKEN = (
    "IQoJb3JpZ2luX2VjEEsaCXVzLXdlc3QtMiJGMEQCIHqd3rKdYDzyq3EWhM2YoeoN6UIo"
    "HmQDFzDjegpB6a7sAiB1HPKJZvuf9VODDunh4YDPR+nYQeG4OftLMlnuULSTGiqgAggU"
    "EAEaDDE2OTMwMTQ0MDk0MyIMA8/Z8FDybWsM3U//Kv0BTOUVWJ2SJTwaAvcQ9ShlufMa"
    "E7qFiSMtoCDjTeFi/0qQB/39VTdItZR0zNXUSi0TYF0RhNbI/38bjictuPo8eeJEt0mJ"
    "NiCAUY6w+SOiqSl/RvQPLAmp/8r15kJfsqxWnBYkSyWShqs4yMCgcJlESl3XAg5ilassy"
    "OW6X8lU09MxWxQaKEvl2jKmosE5IE57clOsw0TyKwZVUrLPg5SifhKyVAJz/qX7EPFXzp"
    "9QhvFbs7YvYMc+ZA8r3aZcp8LmVZrPK+8wajZ1mZnmSLIdJfuafEDrWExnAVy6QnOk/MQ"
    "wjX8u6sTUcvWM6e1Bk6SXs9aZl7gy9shMGCLxdjCpsJrWBjqeAabzKnzGYJMo7h5WzcUs"
    "veQHl8wkLEVHmg+6J8DWH4zyQWwGTFkSkfwwKCNbiAKv+nSOLw8u0T0zSLcFQs0mzbu8Z"
    "ZiO+LzS2eFRFC/8hcDnT5/obk1My/87jKXGd20rX6ZIrRztFM4cHnb1RGnpPIVLj3SZVe"
    "bfnKb12QUtzVOnm5SFTdRodgbrajM/prpmhb9oLvOlJ5hsM3Xj+beM"
)

BUCKET_NAME = "aws-academy-datacenter-bucket-23-02-011"
REGION_NAME = "us-west-2"  # Usamos la región del token para que coincida la firma de sesión

def generar_y_subir():
    try:
        # Configuramos boto3 para que maneje la firma correctamente en us-west-2
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
