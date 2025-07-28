from sqlalchemy import create_engine #create database engine
from sqlalchemy.orm import sessionmaker #factory for creating new sessions
from sqlalchemy.ext.declarative import declarative_base #base class for all models

from core.config import settings

engine = create_engine(
    settings.DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #bind session to engine

Base = declarative_base() #inherit from this class to create models

def get_db(): #gives access to database session, ensure no two sessions are open at the same time
    db = SessionLocal() #create new session
    try:
        yield db #yield db for use in dependencies
    finally:
        db.close() #close session

def create_tables():
    Base.metadata.create_all(bind=engine) #create all tables if they don't exist


