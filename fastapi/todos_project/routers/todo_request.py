from pydantic import BaseModel
from pydantic.fields import Field


class ToDoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length = 3,max_length=100)
    priority:int = Field(ge=1,le=5)
    complete: bool
    
    class Config:
        schema_extra={
            "example":{
                "title":"To do test1",
                "description": "To do description",
                "priority": 1,
                "complete": False 
            }
        }
