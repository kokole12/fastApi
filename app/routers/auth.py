from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2
from .. import utils



router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    # return username and password

    user = db.query(models.AppUser).filter(models.AppUser.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
         detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = oauth2.create_token(data = {"user_id": user.id})
    return{"access_token": access_token, "token_type": "bearer"}
    
    #create token and return token
    # access_token = oauth2.Create_access_token(data = {"user_id": user.id})
    # return {"Access_token": access_token, "token_type": "bearer"}
     


