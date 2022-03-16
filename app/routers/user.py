import psycopg2
from fastapi import  Depends, status, HTTPException, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['users']
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def CreateUser(user: schemas.UserCreate,db:Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_User = models.AppUser(
        **user.dict()
    )
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.AppUser).filter(models.AppUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"user with id {id} not found")
    return user

