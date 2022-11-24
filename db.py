from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from config import MYSQL_URL


engine = create_engine(MYSQL_URL)
Base = declarative_base()
session = sessionmaker(autocommit=False, bind=engine, autoflush=True)


def get_session():
    return session()