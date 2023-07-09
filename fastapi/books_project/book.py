from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


class Book:
    def __init__(self,id:int, title:str,author:str, description:str,rating:int,published_date:date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="This is not required") # if the incoming body didn't contain id, python will give the None and show null in API response
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3,max_length=100)
    rating: int = Field(gt=0,lt=6)
    published_date: date

    class Config:
        schema_extra={
            "example":{
                "title":"a new book",
                "author":"kevin",
                "description":"this is description",
                "rating": 5,
                "published_date":date(2023,12,2)
            }
        }