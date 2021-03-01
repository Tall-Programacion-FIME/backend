from decouple import config

ENVIRONMENT = config("ENVIRONMENT")
DB_URL = config("DATABASE_URL")

DOCS_CONFIG = {
    'openapi_url': '/openapi.json',
    'docs_url': '/docs',
    'redoc_url': '/redoc'
}

if ENVIRONMENT == "PRODUCTION":
    DOCS_CONFIG = {key: None for key in DOCS_CONFIG}
