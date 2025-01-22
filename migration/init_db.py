from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.db import mysql_engine
from app.models.user_model import UserOrm
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

with Session(mysql_engine) as session:
    if session.scalar(select(func.count()).select_from(UserOrm)):
        print("초기유저 존재")
        quit()

    # 초기 유저
    initial_user = UserOrm(
        email=settings.INIT_USER_EMAIL,
        hashed_password=pwd_context.hash(settings.INIT_USER_PASSWORD,),
    )

    session.add(initial_user)
    session.commit()
