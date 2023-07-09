from fastapi import FastAPI
#from starlette import status == from fastapi import status

import models
from database import engine

# import router to be included in the main python module
from routers import auth,todos,admin,user,address

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# main app inlcude sub router or include other controller in the partial class smth like that
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(address.router)


