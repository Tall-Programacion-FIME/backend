from fastapi import APIRouter

from .endpoints import main, user


router = APIRouter()
router.include_router(main.router)
router.include_router(user.router, prefix="/users")
