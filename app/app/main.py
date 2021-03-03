from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT

from .core.settings import settings
from .routers.api import router


@AuthJWT.load_config
def get_config():
    return settings


app = FastAPI(**settings.docs_config)

app.include_router(router)
