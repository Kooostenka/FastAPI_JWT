import os
import uvicorn
from typing import List
from dotenv import load_dotenv

from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi import FastAPI
import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm
import services as _services
import schema as _schemas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/api/users")
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400,
            detail="User with that email already exists")

    user = await _services.create_user(user=user, db=db)

    return await _services.create_token(user=user)


@app.post("/api/token")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user=user)


@app.get("/api/all_users", response_model=List[_schemas.User])
async def get_all(users: _schemas.User = _fastapi.Depends(_services.get_all_users)):
    return users


@app.get("/api/users/me", response_model=_schemas.UserAnswer)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@app.patch("/api/update", response_model=_schemas.UserUpdate)
async def update_users(user: _schemas.UserUpdate = _fastapi.Depends(_services.update_user)):
    return user


@app.delete("/api/delete", response_model=_schemas.UserDelete)
async def delete_users(user: _schemas.UserDelete = _fastapi.Depends(_services.delete_user)):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
