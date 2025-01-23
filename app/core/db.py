from mongoengine import connect, disconnect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.settings import settings

mysql_engine = create_engine(settings.DB_URL, echo=True)


def get_db_session():
    with Session(mysql_engine) as session:
        yield session


def get_mongo_conn():
    print(1111111)
    conn = connect(
        db=settings.MONGO_DB_NAME,
        alias="default",
        host=settings.MONGODB_URI
    )
    print(22222222)
    try:
        yield conn
        print(33333)
    finally:
        disconnect(alias="default")
