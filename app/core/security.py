from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from app.core.settings import settings
from app.enums.security_enums import TokenAuth
from app.enums.security_enums import TokenType
from app.schemas.user_schemas import JwtPayLoad

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# 평문을 해시값으로
def create_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

# 평문과 해시값 비교
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# jwt token 생성
def create_jwt(user_id: int, token_type: str) -> str:
    exp_sec = settings.ACCESS_TOKEN_EXPIRE_SECS if token_type == TokenType.ACCESS else settings.REFRESH_TOKEN_EXPIRE_SECS
    exp_datetime = datetime.now(tz=timezone.utc) + timedelta(seconds=exp_sec)
    jwt_payload = JwtPayLoad(user_id=user_id, exp=exp_datetime, token_type=token_type)
    return jwt.encode(
        jwt_payload.model_dump(),
        settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

# jwt token decode
def decode_jwt(jwt_token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(jwt_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError

# header로 넘어온 jwt token 디코딩
def decode_access_token(scheme: str, param: str) -> JwtPayLoad:
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TokenAuth.INVALID_AUTH_SCHEME
        )

    try:
        payload = payload = decode_jwt(jwt_token=param)
        return JwtPayLoad(
            user_id=payload["user_id"],
            exp=payload["exp"],
            token_type=payload["token_type"]
        )
    # token이 만료되면
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=TokenAuth.TOKEN_EXPIRED)
    # token 검증이 실패하면
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=TokenAuth.INVALID_TOKEN)


# router 요청에 따른 token 검증 디펜던시
def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)) -> JwtPayLoad:
    return decode_access_token(credentials.scheme, credentials.credentials)
