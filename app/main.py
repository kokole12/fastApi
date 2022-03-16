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




# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='post', user='postgres', password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('db connection success')
#         break
#     except Exception as e:
#         print('db connection failed')

# my_post  = [{"title": "first post", "content": "this is the first post on this site", "id": 1},
#  {"title": "second poat", "content": "this is the second post on thi site", "id":2}]


# @app.get('/sqlalchemy')
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{"data": posts} 
@app.get("/")
def root():
   
    return {"mesage": "hello world"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)