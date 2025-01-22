from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.settings import settings

mysql_engine = create_engine(settings.DB_URL, echo=True)
mongo_client = MongoClient(settings.MONGODB_URI)


def get_db_session():
    with Session(mysql_engine) as session:
        yield session


# def get_mongo_db():
#     db = mongo_client["your_database_name"]  # 데이터베이스 이름
#     try:
#         yield db
#     finally:
#         client.close()  #