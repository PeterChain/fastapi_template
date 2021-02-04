from typing import Optional, List
from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserUpdateIn(BaseModel):
    username: str
    password: str
    active: bool
    name: str
    surname: str


class UserOut(BaseModel):
    username: str
    active: bool
    name: str
    surname: str
    admin: bool