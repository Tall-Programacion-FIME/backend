from fastapi import FastAPI
from decouple import config


PRODUCTION = config("PRODUCTION", default=False)
CONFIG = {
    'openapi_url': '/openapi.json',
    'docs_url': '/docs',
    'redoc_url': '/redoc'
}

if PRODUCTION:
    CONFIG = {key: None for key in CONFIG}

app = FastAPI(**CONFIG)


@app.get("/")
async def root():
    return {"message": "Hello world"}
