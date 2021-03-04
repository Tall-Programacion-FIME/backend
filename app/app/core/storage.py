from minio import Minio

from .settings import settings

IS_PRODUCTION = True if settings.ENVIRONMENT == "PRODUCTION" else False

client = Minio(
    endpoint="s3.amazonaws.com" if IS_PRODUCTION else "minio:9000",
    access_key=settings.AWS_ACCESS_KEY,
    secret_key=settings.AWS_SECRET_KEY,
    secure=IS_PRODUCTION,
    region=settings.REGION if IS_PRODUCTION else None
)
