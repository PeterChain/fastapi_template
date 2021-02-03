from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.schemas import users as schemas
from app.services.token import Token
from app.dependencies import authenticate_user, get_db

router = APIRouter()


@router.post("/token", response_model=schemas.TokenOut)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = Token.create(user)
    return {
        "access_token": token.access_token, 
        "token_type": "bearer"
    }
