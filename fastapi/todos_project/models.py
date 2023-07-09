from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database import Base

#from sqlalchemy import Column,Integer,String,Boolean

# indirectly import, sqlalchemy is package.
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer,String, Boolean

class Users(Base):

    __tablename__ = "users"

    id=Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String,unique=True)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String,nullable=True)
    address_id = Column(Integer,ForeignKey("address.id"),nullable=True)
    
    # create relationship between two tables
    address = relationship("Address",back_populates="user_address")
    todos = relationship("Todos",back_populates="owner")


class Todos(Base):

    # tell sqlalchemy that create table in the db.
    __tablename__ = "todos"

    # define the schema.
    id = Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("Users",back_populates="todos")

class Address(Base):
     # tell sqlalchemy that create table in the db.
    __tablename__ = "address"

    # define the schema.
    id = Column(Integer,primary_key=True,index=True)
    address1=Column(String)
    address2=Column(String)
    city=Column(String)
    state=Column(String)
    country=Column(String)
    postalcode=Column(String)
    apt_num = Column(String)

    user_address = relationship("Users",back_populates="address")