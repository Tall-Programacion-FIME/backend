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


@router.post("/token", response_model=schemas.Token, responses={
    401: {
        "description":  "Incorrect username or password"
    }
})
async def login_for_access_token(user: schemas.UserToken, authorize: AuthJWT = Depends(),
                                 db: Session = Depends(get_db)):
    """
    Obtener un token de autorización y un token de actualización
    """
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


@router.post("/refresh_token", response_model=schemas.TokenBase)
async def refresh_old_token(authorize: AuthJWT = Depends()):
    """
    Obtener un nuevo token con el token de actualización.
    El token de actualización se envia en la cabezera de autorización como un token 'Bearer'
    """
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
