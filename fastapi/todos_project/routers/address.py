import sys
from typing_extensions import Annotated

from fastapi import Depends, APIRouter,HTTPException,status
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session

from .auth import get_current_user
from .address_request import AddressRequest

router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={404:{"description":"Not Found"}}
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

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_address(address_request:AddressRequest,
                         db:db_deps,
                         user:user_deps):
    if user is None:
        raise HTTPException(40,"User is unauthorized")

    # create orm model
    address_model = models.Address()

    # DTO maps
    address_model.address1 = address_request.address1
    address_model.address2 = address_request.address2
    address_model.city = address_request.city
    address_model.state = address_request.state
    address_model.country = address_request.country
    address_model.postalcode = address_request.postalcode
    address_model.apt_num = address_request.apt_num

    db.add(address_model)
    db.flush() # kind of like commit but not commit and get the its identity column which is a key

    # update user ids
    user_model = db.query(models.Users).filter(models.Users.id==user.get("user_id")).first()
    user_model.address_id = address_model.id
    db.add(user_model)
    db.commit()

