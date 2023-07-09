from fastapi import APIRouter,Depends, status, HTTPException
from typing_extensions import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import Todos

"""
Start It up
"""
router = APIRouter(
    prefix="/admin",
    tags=["admin"]
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

@router.get("/todos",status_code=status.HTTP_200_OK)
async def get_all_todos(user:user_deps,db: db_deps):  #
    if user is None:
        raise HTTPException(status_code=401,detail=f"Unauthorized")
    if user.get("user_role").lower() != "admin":
        raise HTTPException(status_code=401,detail=f"Unauthorized Resorce Access")
    # only admin can query all the todos, not limited to the user-specific access
    return db.query(Todos).all()

@router.delete("/todos/{todos_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(user:user_deps,db: db_deps,todos_id:int):
    if(user == None or user.get("user_role").lower()!="admin"):
        raise HTTPException(status_code=401,detail=f"Unauthorized")
    todo = db.query(Todos).filter(Todos.id == todos_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail=f"Todo with id {todos_id} not found.")
    db.delete(todo)
    db.commit()
    
    




