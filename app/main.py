import psycopg2
from psycopg2.extras import RealDictCursor
from typing import  List
from fastapi import  Depends, FastAPI,Response, status, HTTPException
from . import models, schemas, utils
from .database import engine, sessionLocal, Base
from sqlalchemy.orm import Session
from .database import get_db
from .routers import post, user, auth



models.Base.metadata.create_all(bind = engine)

app = FastAPI()


@app.get("/")
def root():
   
    return {"mesage": "hello world"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)