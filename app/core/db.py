from mongoengine import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.settings import settings

mysql_engine = create_engine(settings.DB_URL, echo=True)
connect(db='adoc', host='mongodb://adoc:adoc@mongodb-container.docker:27017/adoc?authSource=admin', maxPoolSize=100)


def get_db_session():
    with Session(mysql_engine) as session:
        yield session

def get_mongo_conn():
    yield
