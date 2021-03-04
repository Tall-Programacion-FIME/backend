from fastapi import APIRouter

from .endpoints import auth, user, book

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/user", tags=["user"])
router.include_router(book.router, prefix="/book", tags=["books"])
