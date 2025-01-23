from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.core.security import get_current_user_info
from app.enums.common_enums import ResultMessage
from app.enums.security_enums import TokenAuth
from app.exceptions.user_exception import user_exception_handler
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
    if signup_rst.message != ResultMessage.SUCCESS:
        user_exception_handler(detail=signup_rst.message)

    return BaseResponse(message=signup_rst.message, status_code=status.HTTP_200_OK)


@user_router.post("/login")
def login_user(
    login_info: LoginRequest, db: Annotated[Session, Depends(get_db_session)]
) -> LoginResponse:
    login_rst = user_service.login_user(login_info=login_info, db=db)
    if login_rst.message != ResultMessage.SUCCESS:
        user_exception_handler(detail=login_rst.message)

    return LoginResponse(
        message=login_rst.message, status_code=status.HTTP_200_OK, user_id=login_rst.user_id,
        access_token=login_rst.access_token, refresh_token=login_rst.refresh_token
    )


@user_required_router.post("/refresh")
def refresh_user(
    refresh_body: RefreshRequest,
    jwt_payload: Annotated[JwtPayLoad, Depends(get_current_user_info)],
    db: Annotated[Session, Depends(get_db_session)]
) -> RefreshResponse:
    if refresh_body.user_id != jwt_payload.user_id:
        user_exception_handler(detail=TokenAuth.INVALID_TOKEN)

    get_refresh_rst = user_service.refresh_user(refresh_body=refresh_body, db=db)
    if get_refresh_rst.message != ResultMessage.SUCCESS:
        user_exception_handler(detail=get_refresh_rst.message)

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
        user_exception_handler(detail=TokenAuth.INVALID_TOKEN)

    # logout은 refresh token을 삭제 진행
    logout_rst = user_service.logout_user(logout_body=logout_body, db=db)
    if logout_rst.message != ResultMessage.SUCCESS:
        user_exception_handler(detail=logout_rst.message)

    return BaseResponse(message=logout_rst.message, status_code=status.HTTP_200_OK)
