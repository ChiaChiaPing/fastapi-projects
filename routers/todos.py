from fastapi.responses import HTMLResponse

from starlette.responses import RedirectResponse
from starlette import status
import sys
sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user

from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

# templates folder is in the same hierarchy as main.py
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/",response_class=HTMLResponse)
async def read_all_by_users(request:Request, db: Session = Depends(get_db)):

    # add authentication check for each todo resource

    user = await get_current_user(request)

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

    return templates.TemplateResponse("home.html",{"request":request,"todos":todos, "user":user})

@router.get("/add-todo",response_class=HTMLResponse)
async def add_new_todo(request:Request):

    # add authentication check for each todo resource
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("add-todo.html",{"request":request})

@router.post("/add-todo",response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...), description:str=Form(...),
                      priority:int = Form(...), db:Session = Depends(get_db)):
    
    # add authentication check for each todo resource
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo = models.Todos()
    todo.title = title
    todo.description = description
    todo.priority = priority
    todo.owner_id = user.get("id")
    todo.complete = False
    
    db.add(todo)
    db.commit()

    # actually we call handler that handle /todos ( because we have todos as prefix, so will '/' will be invoked)
    return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)

@router.get("/edit-todo/{todo_id}",response_class=HTMLResponse)
async def edit_todo(request:Request,todo_id:int,db:Session = Depends(get_db)):

    # add authentication check for each todo resource
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first() 

    return templates.TemplateResponse("edit-todo.html",{"request":request,"todo":todo, "user":user})


@router.post("/edit-todo/{todo_id}",response_class=HTMLResponse)
async def edit_todo_commit(request:Request,todo_id:int, title:str = Form(...), description:str=Form(...),
                    priority:int=Form(...), db:Session = Depends(get_db)):
    
    # add authentication check for each todo resource
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}",response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id:int,db:Session = Depends(get_db)):

    # add authentication check for each todo resource
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id) \
                    .filter(models.Todos.owner_id == user.get("id")) \
                    .first()
    

    if todo_model is None:
        return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)
    
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    db.delete(todo_model)
    db.commit()

    return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)

@router.get("/complete/{todo_id}",response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id:int,db:Session = Depends(get_db)):

    # add authentication check for each todo resource
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    todo_model.complete = not todo_model.complete 

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)
