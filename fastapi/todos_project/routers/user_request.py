from pydantic import BaseModel, SecretStr
from pydantic.fields import Field

class UserRequest(BaseModel):
    password: str = Field(min=5)
