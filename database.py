from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sqlite
#SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# PostgeSQL: need hide password bro
SQLALCHEMY_DATABASE_URL = "postgresql://dpzseuxc:m84zSOdGO_DQ6khgs5C8B9_gUj9J93WX@john.db.elephantsql.com/dpzseuxc"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
