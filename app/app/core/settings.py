from decouple import config

PRODUCTION = config("PRODUCTION", default=False)
DOCS_CONFIG = {
    'openapi_url': '/openapi.json',
    'docs_url': '/docs',
    'redoc_url': '/redoc'
}

if PRODUCTION:
    DOCS_CONFIG = {key: None for key in DOCS_CONFIG}
