from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.settings import settings

mysql_engine = create_engine(settings.DB_URL, echo=True)


def get_db_session():
    with Session(mysql_engine) as session:
        yield session
