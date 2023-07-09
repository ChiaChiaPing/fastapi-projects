from fastapi import APIRouter,Depends, status, HTTPException
from datetime import datetime, timedelta
from typing_extensions import Annotated
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from routers.auth_request import CreateUserRequest
from routers.token_response import TokenResponse

from jose import jwt,JWTError


# for hashing function
schemes = "bcrypt"
deprecated = "auto"
bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#openssl rand -hex 32
ALG = "HS256"
SECRET =  "6450c0090018788c667a873f697927946d884a35341635f81f54751c212606c7"

oauth2_bearer = Annotated[str,Depends(OAuth2PasswordBearer(tokenUrl="auth/token"))]


def create_acces_token(username:str, user_id:int,user_role:str,timedelta:timedelta):
    # create user's claim
    encode = {"sub":username,"id":user_id,"role":user_role}
    expired_date = datetime.utcnow() + timedelta
    encode.update({"exp":expired_date})
    return jwt.encode(encode,key=SECRET,algorithm=ALG)


def get_db():
    db = SessionLocal() # use object as functor, this will invoke the __call__ of sessionmaker
    try:
        yield db
    finally:
        # when performing the request fininsh then will close
        db.close()
        
db_deps = Annotated[Session,Depends(get_db)]

def authenticate_user(username:str,password:str,db:db_deps) -> Users:
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return None
    return user if bcrypt_context.verify(password,user.hashed_password) else None

# this is part where the server to validate the token of header is valid or invalid.
async def get_current_user(token:oauth2_bearer):
    try:
        # decrypt with hash alg(not mean non-reversible hash here) -> decode the payload
        decode = jwt.decode(token,key=SECRET,algorithms=[ALG])
        username = decode.get("sub")
        user_id = decode.get("id")
        user_role = decode.get("role")
        if username is None or user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,f"is not authorized")
        return {"username":username,"user_id":user_id,"user_role":user_role}
    except JWTError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,details=e)

"""
Start It up
"""
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_deps,create_user_request:CreateUserRequest):
    try:
        # convert Requests to the ORM users
        create_user_model = Users(
            email = create_user_request.email,
            username = create_user_request.username,
            last_name = create_user_request.last_name,
            first_name = create_user_request.first_name,
            hashed_password = bcrypt_context.hash(create_user_request.password),
            role = create_user_request.role,
            phone_number = create_user_request.phone_number,
            is_active = True
            # role assign null first
        )

        db.add(create_user_model)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.post("/token",response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                db:db_deps):
    auth_user = authenticate_user(form_data.username,form_data.password,db)
    if auth_user is None:
        raise HTTPException(401,f"{form_data.username} is not authenticated.")
    access_token = create_acces_token(auth_user.username,auth_user.id,auth_user.role,timedelta(minutes=20))
    return {"access_token":access_token,"token_typess":"bearer"}

