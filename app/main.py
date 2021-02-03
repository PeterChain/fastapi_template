from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.routes.v1 import users, login


app = FastAPI()

app.include_router(login.router)
app.include_router(users.router, prefix="/v1/users")