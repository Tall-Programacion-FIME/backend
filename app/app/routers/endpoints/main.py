import app.schemas as schemas
from app.core.security import authenticate_user
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello world"}


@router.post("/get_token", response_model=schemas.Token)
async def login_for_access_token(user: schemas.UserCreate, authorize: AuthJWT = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = authorize.create_access_token(subject=user.email)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}
