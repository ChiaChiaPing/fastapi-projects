from fastapi import APIRouter,Depends, status, HTTPException,Body
from typing_extensions import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user,bcrypt_context
from models import Users
from .user_request import UserRequest
"""
Start It up
"""
router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal() # use object as functor, this will invoke the __call__ of sessionmaker
    try:
        yield db
    finally:
        # when performing the request fininsh then will close
        db.close()

db_deps = Annotated[Session,Depends(get_db)]
user_deps = Annotated[dict,Depends(get_current_user)]

@router.get("/current",status_code=status.HTTP_200_OK)
async def get_user(user:user_deps,db:db_deps):
    if user is None:
        raise HTTPException(401, detail="Unauthorized")

    u = db.query(Users).filter(Users.id == user.get("user_id")).first()

    username = user.get("username")
    userid = user.get("user_id")
    if u is None:
        raise HTTPException(404, detail=f"{username} is not found with {userid}")
    return u
    
@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_deps,db:db_deps,password_request:UserRequest):
    if user is None:
        raise HTTPException(401, detail="Unauthorized")


    # get the user first.
    u = await get_user(user,db) # users type

    # validate if the password is same or not
    if bcrypt_context.verify(password_request.password,u.hashed_password):
        raise HTTPException(422, detail="The password is used before, please change to different one")
    
    # if different then update
    u.hashed_password = bcrypt_context.hash(password_request.password)

    # refresh the tokenm 


    # perofmr the DML
    db.add(u)
    db.commit()


    




