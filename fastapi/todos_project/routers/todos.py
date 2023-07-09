from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Path,Query
#from starlette import status == from fastapi import status

from sqlalchemy.orm import Session
from models import Todos
from database import SessionLocal 

from .todo_request import ToDoRequest

from .auth import oauth2_bearer,get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"]

)

def get_db():
    db = SessionLocal() # use object as functor, this will invoke the __call__ of sessionmaker
    try:
        yield db
    finally:
        # when performing the request fininsh then will close
        db.close()

# Depends is like dependencies injection, 
# Session is the sqlalchemy's class you want to di, depends(method) is implementation

# define type
db_deps = Annotated[Session,Depends(get_db)]
user_deps = Annotated[dict,Depends(get_current_user)]

@router.get("/todos")
async def get_all_todos(user:user_deps,db: db_deps):  # because the type has already have implementation so no need to take in when invoking the api
    if user is None:
        raise HTTPException(status_code=401,detail=f"Unauthorized")
    return db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()

@router.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo_by_id(user:user_deps,db:db_deps,todo_id:int=Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=401,detail=f"Unauthorized")
    result = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("user_id")).first()
    if not result:
        raise HTTPException(status_code=404,detail=f"Todo with id {todo_id} not found.")
    return result

@router.post("/todos/create",status_code=status.HTTP_201_CREATED)
async def create_todo(users:user_deps,db:db_deps,body: ToDoRequest):
    try:
        if users is None:
            raise HTTPException(401,details="Unauthoriaed.")
        todo_model = Todos(**body.dict(),owner_id = users.get("user_id"))
        db.add(todo_model)
        db.commit() # because we disable auto commit in the sessionlocal
    except Exception as e:
        raise HTTPException(status_code=500,detail=e)

@router.put("/todos/update/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_deps,db:db_deps,body: ToDoRequest,todo_id:int=Path(ge=1)):
    try:
        if user is None:
            raise HTTPException(401,details="Unauthoriaed.")
        
        todo_model = db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id == user.get("user_id")).first()

        if not todo_model:
             raise HTTPException(status_code=404,detail=f"Todo with id {todo_id} not found.")
        
        # sqlalchemy automtically know this model is the retrieved one so we can update the field on the same.
        todo_model.title  = body.title
        todo_model.description = body.description
        todo_model.priority = body.priority
        todo_model.complete = body.complete

        # add or update
        db.add(todo_model)
        db.commit() # because we disable auto commit in the sessionlocal    
    except Exception as e:
        raise e
    

@router.delete("/todos/delete/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_deps,db:db_deps,todo_id:int=Path(ge=1)):
    try:
        todo_model = db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id == user.get("user_id")).first()

        if not todo_model:
             raise HTTPException(status_code=404,detail=f"Todo with id {todo_id} not found.")
        
        # delete
        db.query(Todos).filter(Todos.id==todo_id).delete()
        #db.delete(todo_model)


        db.commit() # because we disable auto commit in the sessionlocal    
    except Exception as e:
        raise e