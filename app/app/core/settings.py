from pydantic import BaseSettings, Field


def set_url(environment: str, dev_value: str) -> str:
    return None if environment == "PRODUCTION" else dev_value


class __Settings(BaseSettings):
    ENVIRONMENT: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    authjwt_secret_key: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    docs_config: dict = None


_settings = __Settings()
_settings.docs_config = {
    'openapi_url': set_url(__Settings().ENVIRONMENT, '/openapi.json'),
    'docs_url': set_url(__Settings().ENVIRONMENT, '/docs'),
    'redoc_url': set_url(__Settings().ENVIRONMENT, '/redoc')
}

settings: __Settings = _settings
