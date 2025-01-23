
import jwt
from sqlalchemy.orm import Session

from app.core.security import (
    create_hashed_password,
    create_jwt,
    decode_jwt,
    verify_password,
)
from app.enums.common_enums import ResultMessage
from app.enums.security_enums import TokenAuth, TokenType
from app.enums.user_enums import UserAuth
from app.repositories import user_repository
from app.schemas.user_schemas import (
    LoginRequest,
    LoginResult,
    LogoutRequest,
    LogoutResult,
    RefreshRequest,
    RefreshResult,
    SignUpRequest,
    SignupResult,
)


def signup_user(signup_info: SignUpRequest, db: Session) -> SignupResult:
    user = user_repository.get_user_info(
        email=signup_info.email,
        db=db
    )
    if user:
        return SignupResult(message=UserAuth.ALREADY_USER)

    hashed_password = create_hashed_password(plain_password=signup_info.password)
    signup_rst = user_repository.user_signup(
        email=signup_info.email,
        hashed_password=hashed_password,
        db=db
    )

    return signup_rst


def login_user(login_info: LoginRequest, db: Session) -> LoginResult:
    user = user_repository.get_user_refresh_token(
        email=login_info.email,
        db=db
    )
    # 존재하지 않는 유저
    if user is None:
        return LoginResult(message=UserAuth.NO_USER_FOUND)

    # 암호가 다르면
    if not verify_password(plain_password=login_info.password, hashed_password=user.hashed_password):
        return LoginResult(message=UserAuth.INVALID_PASSWORD)

    try:
        refresh_token = user.refresh_token
        # login한 계정의 refresh token 없으면 token 생성
        if not refresh_token:
            raise ValueError
        # refresh token decode error 발생하면 token 생성
        _ = decode_jwt(jwt_token=user.refresh_token)
    except (jwt.exceptions.PyJWTError, ValueError):
        # 만료 또는 잘못된 refresh이거나 refresh token 자체가 없으면 db에 upsert
        refresh_token = create_jwt(user_id=user.id, token_type=TokenType.REFRESH)
        login_rst = user_repository.upsert_refresh_token(
            user_id=user.id,
            refresh_token=refresh_token,
            db=db
        )
        if login_rst.message != ResultMessage.ERROR:
            login_rst.user_id = user.id
            login_rst.refresh_token = refresh_token
            login_rst.access_token = create_jwt(user_id=user.id, token_type=TokenType.ACCESS)
    else:
        login_rst = LoginResult(
            message=ResultMessage.SUCCESS,
            user_id=user.id,
            access_token=create_jwt(user_id=user.id, token_type=TokenType.ACCESS),
            refresh_token=refresh_token
        )

    return login_rst


def refresh_user(refresh_body: RefreshRequest, db: Session) -> RefreshResult:
    db_refresh_token = user_repository.verify_refresh_token(refresh_body=refresh_body, db=db)
    # refresh token and user_id 결과가 none인 경우
    if not db_refresh_token:
        return RefreshResult(message=TokenAuth.INVALID_TOKEN)

    try:
        payload = decode_jwt(jwt_token=refresh_body.refresh_token, token_type=TokenType.REFRESH)
        access_token = create_jwt(user_id=payload["user_id"], token_type=TokenType.ACCESS)
        return RefreshResult(message=ResultMessage.SUCCESS, access_token=access_token)
    except jwt.ExpiredSignatureError:
        return RefreshResult(message=TokenAuth.TOKEN_EXPIRED)
    except jwt.InvalidTokenError:
        return RefreshResult(message=TokenAuth.INVALID_TOKEN)


def logout_user(logout_body: LogoutRequest, db: Session) -> LogoutResult:
    return user_repository.refresh_token_to_null(logout_body=logout_body, db=db)
