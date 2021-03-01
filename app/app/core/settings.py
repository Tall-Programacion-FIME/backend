from decouple import config

# Current environment
ENVIRONMENT = config("ENVIRONMENT")

# Database
DB_URL = config("DATABASE_URL")

# API docs configuration
DOCS_CONFIG = {
    'openapi_url': '/openapi.json',
    'docs_url': '/docs',
    'redoc_url': '/redoc'
}

if ENVIRONMENT == "PRODUCTION":
    DOCS_CONFIG = {key: None for key in DOCS_CONFIG}
