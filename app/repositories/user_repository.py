
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from app.models.user_model import UserOrm, RefreshTokenOrm
from sqlalchemy import select
from datetime import datetime, timezone
from app.schemas.user_schemas import SignupResult, LoginResult


def get_user_info(email: str, db: Session) -> UserOrm | None:
    # 이메일 존재 여부 확인
    user_query = select(UserOrm).where(UserOrm.email == email).limit(1)
    return db.scalar(user_query)


def user_signup(email: str, hashed_password: str, db: Session) -> SignupResult:
    # 아이디가 존재하는 경우
    input_user = get_user_info(email=email, db=db)
    if input_user:
        return SignupResult(message="already user", user=input_user)
    
    # db에 회원가입 요정 아이디 비밀번호 insert 진행
    new_user = UserOrm(email=email, hashed_password=hashed_password, created_at=datetime.now())
    try:
        db.add(new_user)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        return SignupResult(message="error", user=None)
    else:
        return SignupResult(message="success", user=new_user)


def upsert_refresh_token(
    user: UserOrm, refresh_token: str, refresh_exp: datetime, db: Session
) -> LoginResult:
    now = datetime.now(tz=timezone.utc)
    insert_query = insert(RefreshTokenOrm).values(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=refresh_exp,
        created_at=now
    )
    update_query = insert_query.on_duplicate_key_update(
        refresh_token=insert_query.inserted.refresh_token,
        expires_at=insert_query.inserted.expires_at,
        updated_at=now
    )
    db.execute(update_query)
    db.commit()
    return LoginResult(message="test")
