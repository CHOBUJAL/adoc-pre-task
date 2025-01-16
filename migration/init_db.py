from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.db import engine
from app.settings import settings
from app.models.user_model import UserOrm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

with Session(engine) as session:
    if session.scalar(select(func.count()).select_from(UserOrm)):
        print("초기유저 존재")
        quit()

    # 초기 유저
    initial_user = UserOrm(
        name=settings.INIT_USER_NAME,
        phone_number=settings.INIT_USER_PHONE_NUM,
        email=settings.INIT_USER_EMAIL,
        hashed_password=pwd_context.hash(settings.INIT_USER_PASSWORD,),
        address=settings.INIT_USER_ADDR,
    )

    session.add(initial_user)
    session.commit()
