from pydantic import BaseModel
from typing import Optional

class AddressRequest(BaseModel):
    address1:str
    address2:Optional[str]
    city:str
    state:str
    country:str
    postalcode:str
    apt_num:Optional[str]