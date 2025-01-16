from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.settings import settings

engine = create_engine(settings.DB_URL, echo=True)


def get_db_session():
    with Session(engine) as session:
        yield session
