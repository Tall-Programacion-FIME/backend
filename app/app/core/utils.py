from .settings import settings


def is_valid_email_domain(email: str) -> bool:
    if "@uanl.edu.mx" not in email:
        return False
    return True


def get_file_url(filename: str) -> str:
    if settings.ENVIRONMENT == "PRODUCTION":
        return f"https://cdn.uanl.store/{filename}"  # pragma: no cover
    elif settings.ENVIRONMENT == "DEVELOPMENT":
        return f"http://localhost:9000/{settings.BUCKET_NAME}/{filename}"


def send_verification_email(verification_token: bytes):
    print(verification_token)
