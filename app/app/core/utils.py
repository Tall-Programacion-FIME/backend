import boto3

from .settings import settings

PRODUCTION = settings.ENVIRONMENT == "PRODUCTION"


def is_valid_email_domain(email: str) -> bool:
    if "@uanl.edu.mx" not in email:
        return False
    return True


def get_file_url(filename: str) -> str:
    if settings.ENVIRONMENT == "PRODUCTION":
        return f"https://cdn.uanl.store/{filename}"  # pragma: no cover
    elif settings.ENVIRONMENT == "DEVELOPMENT":
        return f"http://localhost:9000/{settings.BUCKET_NAME}/{filename}"


def send_verification_email(
    *, verification_token: bytes, email_address: str, name: str
):
    verification_token = verification_token.decode("utf-8")
    if PRODUCTION:
        url = f"https://fime.uanl.store/auth/verify/{verification_token}"
    else:
        url = f"http://localhost:3000/auth/verify/{verification_token}"

    email_data = (
        f"Hola {name}! Gracias por crear tu cuenta en <b>FIME sobre ruedas</b>\n"
        f"Para activar tu cuenta haz click en este <a href='{url}'>enlace</a>"
    )
    if PRODUCTION:
        _send_email(email_address, email_data)
    else:
        print(email_data)


def _send_email(email_address: str, content):
    ses = boto3.client(
        "sesv2",
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
        region_name="us-east-1",
    )
    ses.send_email(
        FromEmailAddress="no-reply@uanl.store",
        FromEmailAddressIdentityArn="arn:aws:ses:us-east-1:254716461375:identity/no-reply@uanl.store",
        Destination={"ToAddresses": [email_address]},
        Content={
            "Simple": {
                "Subject": {"Data": "Confirma tu correo en FIME sobre ruedas"},
                "Body": {"Html": {"Data": content}},
            }
        },
    )
