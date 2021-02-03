from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from app.database import SessionLocal
from app.models import users
from app.services.token import Token
from app.schemas.users import UserOut


### Database dependencies

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


### Authentication dependencies

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_password(password: str, db_password: str):
    return pwd_context.verify(password, db_password) 


def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)


def get_logged_user(
    token: str = Depends(oauth_scheme), 
    db: Session = Depends(get_db)
) -> UserOut:
    access_token = Token(token)
    username = access_token.get_username()
    if not username:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Token"
        )
    db_user = db.query(users.User).get(username)
    return UserOut(
        username=db_user.username,
        name=db_user.name,
        surname=db_user.surname,
        active=db_user.active
    )


def authenticate_user(
    db: Session,
    username: str, 
    password: str
) -> users.User:
    # Does the user exists?
    db_user = db.query(users.User).get(username)
    if not db_user:
        return None
    
    # Does the password match?
    hash_passwd = hash_password(password)
    if check_password(hash_passwd, db_user.hashed_password):
        return None

    # Is the user active?
    if not db_user.active:
        return None
    
    return db_user