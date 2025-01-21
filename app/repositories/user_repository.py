
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.user_model import UserOrm
from sqlalchemy import select
from datetime import datetime
from app.schemas.user_schemas import SignupResult, LoginRequest


def get_user_info(email: str, db: Session) -> UserOrm | None:
    # 이메일 존재 여부 확인
    user_query = select(UserOrm).where(UserOrm.email == email).limit(1)
    return db.scalar(user_query)


def user_signup(email: str, hashed_password: str, db: Session) -> SignupResult:
    # 아이디가 존재하는 경우
    input_user = get_user_info(email=email, db=db)
    if input_user:
        return SignupResult(user=input_user, message="already user")
    
    # db에 회원가입 요정 아이디 비밀번호 insert 진행
    new_user = UserOrm(email=email, hashed_password=hashed_password, created_at=datetime.now())
    try:
        db.add(new_user)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        return SignupResult(user=None, message="error")
    else:
        return SignupResult(user=new_user, message="success")


# def upsert_refresh_token(login_info: LoginRequest, db: Session):