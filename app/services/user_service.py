from datetime import datetime, timedelta, timezone
from typing import Tuple

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.schemas.user_schemas import (
    JwtPayLoad,
    LoginRequest,
    RefreshRequest,
    SignUpRequest,
    SignupResult,
)
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# 평문을 해시값으로
def create_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

# 평문과 해시값 비교
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# jwt token 생성
def create_jwt(user_id: int, exp_sec: int, token_type: str) -> Tuple[str, datetime]:
    exp_datetime = datetime.now(tz=timezone.utc) + timedelta(seconds=exp_sec)
    jwt_payload = JwtPayLoad(user_id=user_id, exp=exp_datetime, token_type=token_type)
    return jwt.encode(
        jwt_payload.model_dump(),
        settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    ), exp_datetime

# header로 넘어온 jwt token 디코딩
def decode_access_token(scheme: str, param: str) -> JwtPayLoad:
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid authentication scheme"
        )

    try:
        payload = jwt.decode(param, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return JwtPayLoad(
            user_id=payload["user_id"],
            exp=payload["exp"],
            token_type=payload["token_type"]
        )
    # token이 만료되면
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired")
    # token 검증이 실패하면
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

# router 요청에 따른 token 검증 디펜던시
def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)) -> JwtPayLoad:
    return decode_access_token(credentials.scheme, credentials.credentials)


def signup_user(signup_info: SignUpRequest, db: Session) -> SignupResult:
    hashed_password = create_hashed_password(plain_password=signup_info.password)
    signup_rst = user_repository.user_signup(
        email=signup_info.email,
        hashed_password=hashed_password,
        db=db
    )
    # 존재하는 이메일
    if signup_rst.message == "already user":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already user")
    return signup_rst


def login_user(login_info: LoginRequest, db: Session):# -> LoginResult:
    user = user_repository.get_user_info(
        email=login_info.email,
        db=db
    )
    # 존재하지 않는 유저
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no user found")

    # 암호가 다르면
    if not verify_password(plain_password=login_info.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid password")


    access_token, _ = create_jwt(user_id=user.id, exp_sec=settings.ACCESS_TOKEN_EXPIRE_SECS, token_type="access")
    refresh_token, refresh_exp = create_jwt(user_id=user.id, exp_sec=settings.REFRESH_TOKEN_EXPIRE_SECS, token_type="refresh")

    login_rst = user_repository.upsert_refresh_token(
        user_id=user.id,
        refresh_token=refresh_token,
        refresh_exp=refresh_exp,
        db=db
    )
    login_rst.access_token = access_token
    login_rst.refresh_token = refresh_token
    return login_rst


def refresh_to_access_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return create_jwt(user_id=payload["user_id"], exp_sec=settings.ACCESS_TOKEN_EXPIRE_SECS, token_type="access")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")


def get_new_token(refresh_body: RefreshRequest, db: Session):
    db_refresh_token = user_repository.verify_refresh_token(refresh_body=refresh_body, db=db)
    # refresh token and user_id 결과가 none인 경우
    if not db_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")

    return refresh_to_access_token(refresh_token=refresh_body.refresh_token)
