from fastapi import FastAPI

from .core.settings import DOCS_CONFIG
from .routers.api import router

app = FastAPI(**DOCS_CONFIG)

app.include_router(router)
