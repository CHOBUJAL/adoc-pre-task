from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.core.security import get_current_user_info
from app.enums.common_enums import ResultMessage
from app.enums.security_enums import TokenAuth
from app.enums.user_enums import UserAuth
from app.schemas.user_schemas import (
    BaseResponse,
    JwtPayLoad,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    RefreshRequest,
    RefreshResponse,
    SignUpRequest,
)
from app.services import user_service

user_router = APIRouter(
    prefix="/users",
    tags=["인증이 필요없는 User 관련 라우터"],
)
user_required_router = APIRouter(
    prefix="/users",
    dependencies=[Depends(get_current_user_info)],
    tags=["인증이 필요한 User 관련 라우터"],
)


@user_router.post("/signup")
def signup_user(
    signup_info: SignUpRequest, db: Annotated[Session, Depends(get_db_session)]
) -> BaseResponse:
    signup_rst = user_service.signup_user(signup_info=signup_info, db=db)
    # server error
    if signup_rst.user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=signup_rst.message
        )
    # 이미 있는 유저 정보
    if signup_rst.message == UserAuth.ALREADY_USER:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=UserAuth.ALREADY_USER
        )

    return BaseResponse(message=signup_rst.message, status_code=status.HTTP_200_OK)


@user_router.post("/login")
def login_user(
    login_info: LoginRequest, db: Annotated[Session, Depends(get_db_session)]
) -> LoginResponse:
    login_rst = user_service.login_user(login_info=login_info, db=db)
    # server error
    if login_rst.message == ResultMessage.ERROR:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=login_rst.message
        )
    # 없는 유저 정보
    elif login_rst.message == UserAuth.NO_USER_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=UserAuth.NO_USER_FOUND
        )
    # 잘못된 비밀번호
    elif login_rst.message == UserAuth.INVALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=UserAuth.INVALID_PASSWORD
        )

    return LoginResponse(
        message=login_rst.message, status_code=status.HTTP_200_OK,
        access_token=login_rst.access_token, refresh_token=login_rst.refresh_token
    )


@user_required_router.post("/refresh")
def refresh_user(
    refresh_body: RefreshRequest,
    jwt_payload: Annotated[JwtPayLoad, Depends(get_current_user_info)],
    db: Annotated[Session, Depends(get_db_session)]
) -> RefreshResponse:
    if refresh_body.user_id != jwt_payload.user_id:
        raise HTTPException(status_code=401, detail=TokenAuth.INVALID_TOKEN)

    get_refresh_rst = user_service.refresh_user(refresh_body=refresh_body, db=db)
    # server error
    if get_refresh_rst.message == ResultMessage.ERROR:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ResultMessage.ERROR
        )
    # 유효하지 않은 토큰이면
    elif get_refresh_rst.message == TokenAuth.INVALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=TokenAuth.INVALID_TOKEN
        )
    # 만료된 토큰이면
    elif get_refresh_rst.message == TokenAuth.TOKEN_EXPIRED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=TokenAuth.TOKEN_EXPIRED
        )

    return RefreshResponse(
        message=ResultMessage.SUCCESS, status_code=status.HTTP_200_OK, access_token=get_refresh_rst.access_token
    )


@user_required_router.post("/logout")
def logout_user(
    logout_body: LogoutRequest,
    jwt_payload: Annotated[JwtPayLoad, Depends(get_current_user_info)],
    db: Annotated[Session, Depends(get_db_session)]
) -> BaseResponse:
    # access token이 무효한 경우 refresh token 관련 작업 중지
    if logout_body.user_id != jwt_payload.user_id:
        raise HTTPException(status_code=401, detail=TokenAuth.INVALID_TOKEN)

    # logout은 refresh token을 삭제 진행
    logout_rst = user_service.logout_user(logout_body=logout_body, db=db)
    if logout_rst.message == ResultMessage.ERROR:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=logout_rst.message
        )

    return BaseResponse(message=logout_rst.message, status_code=status.HTTP_200_OK)
