import jwt
from typing import Tuple
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.schemas.user_schemas import SignUpRequest, LoginRequest, SignupResult, LoginResult
from sqlalchemy.orm import Session
from app.repositories import user_repository
from app.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt(user_id: int, exp_sec: int, token_type: str) -> Tuple[str, datetime]:
    exp_datetime = datetime.now(tz=timezone.utc) + timedelta(seconds=exp_sec)
    return jwt.encode(
        {"user_id": user_id, "exp": exp_datetime, "token_type": token_type},
        settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    ), exp_datetime


def signup_user(signup_info: SignUpRequest, db: Session) -> SignupResult:
    hashed_password = create_hashed_password(plain_password=signup_info.password)
    return user_repository.user_signup(
        email=signup_info.email,
        hashed_password=hashed_password,
        db=db
    )
    
def login_user(login_info: LoginRequest, db: Session):# -> LoginResult:
    user = user_repository.get_user_info(
        email=login_info.email,
        db=db
    )
    if user is None:
        return LoginResult(message="no user found")
    
    if not verify_password(plain_password=login_info.password, hashed_password=user.hashed_password):
        return LoginResult(message="invalid password")
    
    
    access_token, _ = create_jwt(user_id=user.id, exp_sec=settings.ACCESS_TOKEN_EXPIRE_SECS, token_type="access")
    refresh_token, refresh_exp = create_jwt(user_id=user.id, exp_sec=settings.REFRESH_TOKEN_EXPIRE_SECS, token_type="refresh")
    
    login_rst = user_repository.upsert_refresh_token(
        user=user,
        refresh_token=refresh_token,
        refresh_exp=refresh_exp,
        db=db
    )
    login_rst.access_token = access_token
    login_rst.refresh_token = refresh_token
    return login_rst
