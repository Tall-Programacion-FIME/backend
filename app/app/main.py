from fastapi import FastAPI

from .core.settings import settings
from .routers.api import router

app = FastAPI(**settings.docs_config)

app.include_router(router)
