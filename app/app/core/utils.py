from .settings import settings


def is_valid_email_domain(email: str) -> bool:
    if "@uanl.edu.mx" not in email:
        return False
    return True


def get_file_url(filename: str) -> str:
    if settings.ENVIRONMENT == "PRODUCTION":
        return f"https://{settings.BUCKET_NAME}.s3.amazonaws.com/{filename}"  # pragma: no cover
    elif settings.ENVIRONMENT == "DEVELOPMENT":
        return f"http://localhost:9000/{settings.BUCKET_NAME}/{filename}"
