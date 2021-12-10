import datetime as _dt
import pydantic as _pydantic
from typing import Optional


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int
    date_created: _dt.datetime

    class Config:
        orm_mode = True


class UserUpdate(_pydantic.BaseModel):
    last_name: str

    class Config:
        orm_mode = True


class UserDelete(_UserBase):
    email: Optional[str]

    class Config:
        orm_mode = True


class UserAnswer(_pydantic.BaseModel):
    id: int
    email: str
    last_name: Optional[str]
    date_created: _dt.datetime

