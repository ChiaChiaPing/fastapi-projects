from pydantic import BaseModel
from typing import Optional

class CreateUserRequest(BaseModel):
    email: str
    username : str
    first_name: str
    last_name: str
    #is_active: bool
    role: str
    password:str
    phone_number:Optional[str]