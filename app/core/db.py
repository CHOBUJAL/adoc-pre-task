from mongoengine import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.settings import settings


mysql_engine = create_engine(settings.DB_URL, echo=True)
connect(db=settings.MONGO_DB_NAME, host=settings.MONGODB_URI)


def get_db_session():
    with Session(mysql_engine) as session:
        yield session

def get_mongo_conn():
    yield None
