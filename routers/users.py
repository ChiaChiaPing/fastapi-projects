import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, status, APIRouter, Request,Response,Form
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user

# this is for JWT authentication
SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# templates folder is in the same hierarchy as main.py
templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"user": "Not authorized!"}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

@router.get("/",response_class=HTMLResponse)
async def get_change_password_page(request:Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth",status=status.HTTP_302_FOUND)
    
    #user = db.query(models.Users).filter(models.Users.username == user.get('id')).first()
    
    return templates.TemplateResponse("change-pwd.html",{"request":request,"user":user}) 

@router.post("/change-password",response_class=HTMLResponse)
async def change_password(request:Request, username:str = Form(...),
                          password:str = Form(...),
                          new_password:str = Form(...),
                          db:Session = Depends(get_db)):
    
    msg = []  
    result_code = True
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth",status=status.HTTP_302_FOUND)
    

    user_model = db.query(models.Users).filter(models.Users.username == username).first()
    if user_model is None:
        msg.append(f"User is not exist with {username}")
        result_code = False

    if not verify_password(password,user_model.hashed_password):
        msg.append(f"The old password is incorrect")
        result_code = False
    
    if password == new_password:
        msg.append(f"The old password and new password cannot not be same, please check")
        result_code = False
    
    if result_code: # pass all validation
        user_model.hashed_password = get_password_hash(new_password)
        msg.append("Change password Successfully")
        db.add(user_model)
        db.commit()
    
    msg = "; ".join(msg)
    return templates.TemplateResponse("change-pwd.html",{"request":request,"msg":msg,
                                                         "user":user,"result_code":result_code}) # True mean success.










