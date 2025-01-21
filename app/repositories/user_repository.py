
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from app.models.user_model import RefreshTokenOrm, UserOrm
from app.schemas.user_schemas import LoginResult, RefreshRequest, SignupResult


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
    except Exception:
        db.rollback()
        return SignupResult(message="error")
    else:
        return SignupResult(message="success", user=new_user)


def upsert_refresh_token(
    user_id: int, refresh_token: str, refresh_exp: datetime, db: Session
) -> LoginResult:
    now = datetime.now(tz=timezone.utc)
    insert_data = {
        "user_id": user_id,
        "refresh_token": refresh_token,
        "expires_at": refresh_exp,
    }
    try:
        upsert_query = insert(RefreshTokenOrm).values(insert_data).on_duplicate_key_update(
            refresh_token=insert_data["refresh_token"],
            expires_at=insert_data["expires_at"],
            updated_at=now,
        )
        db.execute(upsert_query)
        db.commit()
    except Exception:
        db.rollback()
        return LoginResult(message="error")
    else:
        return LoginResult(message="success")


def verify_refresh_token(refresh_body: RefreshRequest, db: Session) -> RefreshTokenOrm | None:
    refresh_query = select(RefreshTokenOrm).where(
        RefreshTokenOrm.user_id == refresh_body.user_id,
        RefreshTokenOrm.refresh_token == refresh_body.refresh_token
    ).limit(1)
    return db.scalar(refresh_query)
