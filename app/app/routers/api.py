from fastapi import APIRouter

from .endpoints import main, user, book

router = APIRouter()
router.include_router(main.router)
router.include_router(user.router, prefix="/user")
router.include_router(book.router, prefix="/book")
