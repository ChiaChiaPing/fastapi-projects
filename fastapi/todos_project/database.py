from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



"""
For Sqllite only
"""
#SQLALCHEMY_URL="sqlite:///./todosapp.db"
#engine = create_engine(SQLALCHEMY_URL,connect_args={"check_same_thread":False})

"""
For MySQL
"""
#<sql platform> + SQlConnector
#SQLALCHEMY_URL="mysql+pymysql://root:rootroot@localhost:3399/ToDoApplicationDatabase"
#engine = create_engine(SQLALCHEMY_URL)

"""
For PostgreSQL
"""
#<sql platform> + SQlConnector
SQLALCHEMY_URL="postgresql://postgres:root@localhost:5435/todosapp"
engine = create_engine(SQLALCHEMY_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False, bind=engine)

# declare the database
Base = declarative_base()