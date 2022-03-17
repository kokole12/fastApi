
from typing import  List, Optional
from fastapi import  Depends,Response, status, HTTPException, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/", response_model=List[schemas.Post])
def first(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), 
limit: int = 10, skip:int = 0, search: Optional[str]= ""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createpost(post: schemas.CreatPost, db:Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    
    created = models.Post(
        user_id = current_user.id, **post.dict()
    )
    db.add(created)

    db.commit()
    db.refresh(created)
    return created


@router.get("/{id}", response_model=schemas.Post)
def getpost(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return  post



@router.delete("/{id}")
def delete_post(id : int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

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
