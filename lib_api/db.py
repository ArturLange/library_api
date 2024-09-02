from collections.abc import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

from lib_api.models import Base

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DBNAME = os.getenv("POSTGRES_DB")

from sqlalchemy.engine import URL

url = URL.create(
    drivername="postgresql+psycopg2",
    username=POSTGRES_USER,
    password=POSTGRES_PASS,
    host=POSTGRES_HOST,
    database=POSTGRES_DBNAME,
)

engine = create_engine(url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)


def get_db() -> Iterator[Session]:
    db = session()
    try:
        yield db
    finally:
        db.close()
