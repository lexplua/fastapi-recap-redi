from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

_engine = None
SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        database_url = os.getenv("DATABASE_URL")
        _engine = create_engine(database_url)
        Base.metadata.create_all(bind=get_engine())
    return _engine


def get_session():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return SessionLocal()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
