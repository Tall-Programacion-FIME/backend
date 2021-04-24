import boto3
from botocore.client import Config

from .settings import settings

IS_PRODUCTION = True if settings.ENVIRONMENT == "PRODUCTION" else False

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    endpoint_url="s3.amazonaws.com" if IS_PRODUCTION else "http://minio:9000",
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)
