import boto3
from botocore.config import Config

BUCKET_NAME = "aws-academy-datacenter-bucket-23-02-011"
REGION_NAME = "us-west-2"

# Boto3 detectará automáticamente tus credenciales desde ~/.aws/credentials
custom_config = Config(region_name=REGION_NAME, signature_version='s3v4')
s3_client = boto3.client(
    's3',
    config=custom_config
)

print("Subiendo archivos locales a la carpeta 'raw/' en S3...")
s3_client.upload_file('raw/transacciones.csv', BUCKET_NAME, 'raw/transacciones.csv')
s3_client.upload_file('raw/logs_m2m.json', BUCKET_NAME, 'raw/logs_m2m.json')
print("-> ¡Archivos subidos con éxito a S3!")
