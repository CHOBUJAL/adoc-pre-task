
from datetime import datetime, timezone
from typing import Any, Dict, List

from sqlalchemy import select, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from app.enums.common_enums import ResultMessage
from app.models.user_model import RefreshTokenOrm, UserOrm
from app.schemas.user_schemas import (
    LoginResult,
    LogoutRequest,
    LogoutResult,
    RefreshRequest,
    SignupResult,
)


def get_user_info(email: str, db: Session) -> UserOrm | None:
    # 이메일 존재 여부 확인
    user_query = select(UserOrm).where(UserOrm.email == email).limit(1)
    return db.scalar(user_query)

def get_user_refresh_token(email: str, db: Session) -> List[Dict[str, Any]]:
    user_query = (
        select(
            UserOrm.id.label("id"),
            UserOrm.hashed_password.label("hashed_password"),
            RefreshTokenOrm.refresh_token.label("refresh_token"),
        )
        .outerjoin(RefreshTokenOrm, UserOrm.id == RefreshTokenOrm.user_id)
        .where(UserOrm.email == email)
    )
    return db.execute(user_query).first()


def user_signup(email: str, hashed_password: str, db: Session) -> SignupResult:
    # db에 회원가입 요청 아이디 비밀번호 insert 진행
    new_user = UserOrm(
        email=email, hashed_password=hashed_password, created_at=datetime.now()
    )
    try:
        db.add(new_user)
        db.commit()
    except Exception:
        db.rollback()
        return SignupResult(message=ResultMessage.ERROR)
    else:
        return SignupResult(message=ResultMessage.SUCCESS, user=new_user)


def upsert_refresh_token(
    user_id: int, refresh_token: str, db: Session
) -> LoginResult:
    now = datetime.now(tz=timezone.utc)
    insert_data = {
        "user_id": user_id,
        "refresh_token": refresh_token,
    }
    try:
        upsert_query = insert(RefreshTokenOrm).values(insert_data).on_duplicate_key_update(
            refresh_token=insert_data["refresh_token"],
            updated_at=now,
        )
        db.execute(upsert_query)
        db.commit()
    except Exception:
        db.rollback()
        return LoginResult(message=ResultMessage.ERROR)
    else:
        return LoginResult(message=ResultMessage.SUCCESS)


def verify_refresh_token(refresh_body: RefreshRequest, db: Session) -> RefreshTokenOrm | None:
    refresh_query = select(RefreshTokenOrm).where(
        RefreshTokenOrm.user_id == refresh_body.user_id,
        RefreshTokenOrm.refresh_token == refresh_body.refresh_token
    ).limit(1)
    return db.scalar(refresh_query)


def refresh_token_to_null(logout_body: LogoutRequest, db: Session) -> LogoutResult:
    try:
        update_query = update(RefreshTokenOrm).where(
                RefreshTokenOrm.user_id == logout_body.user_id,
                RefreshTokenOrm.refresh_token.isnot(None)
            ).values(refresh_token=None)
        db.execute(update_query)
        db.commit()
    except Exception:
        db.rollback()
        return LogoutResult(message=ResultMessage.ERROR)
    else:
        return LogoutResult(message=ResultMessage.SUCCESS)
