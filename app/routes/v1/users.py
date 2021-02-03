from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.schemas import users as schemas
from app.models.users import User
from app.dependencies import (
    get_db, 
    get_logged_user, 
    hash_password
)

router = APIRouter()


@router.get("/", response_model=schemas.UserOut)
def get_user(user: schemas.UserOut = Depends(get_logged_user)):
    return user


@router.post("/", response_model=schemas.UserOut)
def create_user(
    user_to_create: schemas.UserIn, 
    user: schemas.UserOut = Depends(get_logged_user),
    db: Session = Depends(get_db)
):
    # Only a admin user can create other users
    admin_user = db.query(User).get(user.username)
    if not admin_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can create users"
        )
    
    # Username must be unique
    if db.query(User).get(user_to_create.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    new_user = User(**user_to_create.dict())
    new_user.hashed_password = hash_password(user_to_create.password)
    db.add(new_user)
    db.flush()
    db.commit()
    return schemas.UserOut(**new_user.dict())


@router.put("/", response_model=schemas.UserOut)
def update_user(
    user_data: schemas.UserUpdateIn, 
    db: Session = Depends(get_db),
    user: schemas.UserOut = Depends(get_logged_user)
):
    db_user = db.query(User).get(user.username)
    if user_data.name:
        db_user.name = user_data.name
    if user_data.surname:
        db_user.surname = user_data.surname
    if user_data.password:
        db_user = hash_password(user_data.password)
    db.flush()
    db.commit()
    return db_user