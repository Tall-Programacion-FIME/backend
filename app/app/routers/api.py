from fastapi import APIRouter

from .endpoints import main


router = APIRouter()
router.include_router(main.router)
