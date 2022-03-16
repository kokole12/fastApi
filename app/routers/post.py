import psycopg2
from psycopg2.extras import RealDictCursor
from typing import  List
from fastapi import  Depends,Response, status, HTTPException, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/", response_model=List[schemas.Post])
def first(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createpost(post: schemas.CreatPost, db:Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO post (title, content, published) 
    # VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))

    # created = cursor.fetchone()

    # conn.commit()
    # print(current_user.id)
    #created = models.Post(title = post.title, content = post.content, published = post.published)
    created = models.Post(
        user_id = current_user.id, **post.dict()
    )
    db.add(created)

    db.commit()
    db.refresh(created)
    return created

# def find_index_id(id):
#     for i, p in enumerate(my_post):
#         if p["id"] == id:
#          return i

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p



# @app.get("/post/latest")
# def get_latest():
#    post =  my_post[len(my_post)-1]
#    return {"details": post}


@router.get("/{id}", response_model=schemas.Post)
def getpost(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(int(id))

    # cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with Id {id} was not found")
    #     # raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with Id {id} was not found")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f"post with Id {id} was not found"}
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return  post



@router.delete("/{id}")
def delete_post(id : int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # # index = find_index_id(int(id))
    deleted_post_query =  db.query(models.Post).filter(models.Post.id == id)

    deleted_post = deleted_post_query.first()

    if deleted_post== None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no id match")

    if deleted_post.user_id != current_user.id:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorised to perform requested")
   
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updatepost:schemas.CreatPost, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    # (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()

    # conn.commit() 
    post_query = db.query(models.Post).filter(models.Post.id == id )

    post= post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorised to perform requested")
   
    # post_query.update({"title": "post hard coded put", "content": "hardcoded contend"}, synchronize_session=False)
    post_query.update(updatepost.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
