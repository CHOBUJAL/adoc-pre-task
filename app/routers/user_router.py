from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.schemas.user_schemas import (
    JwtPayLoad,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    SignUpRequest,
    SignUpResponse,
)
from app.services import user_service

user_router = APIRouter(
    prefix="/users",
    tags=["인증이 필요없는 User 관련 라우터"],
)
user_required_router = APIRouter(
    prefix="/users",
    dependencies=[Depends(user_service.get_current_user_info)],
    tags=["인증이 필요한 User 관련 라우터"],
)


@user_router.post("/signup")
def signup_user(
    signup_info: SignUpRequest, db: Annotated[Session, Depends(get_db_session)]
) -> SignUpResponse:
    signup_rst = user_service.signup_user(signup_info=signup_info, db=db)
    # server error
    if signup_rst.user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=signup_rst.message
        )

    return SignUpResponse(message=signup_rst.message, status_code=status.HTTP_200_OK)


@user_router.post("/login")
def login_user(
    login_info: LoginRequest, db: Annotated[Session, Depends(get_db_session)]
) -> LoginResponse:
    login_rst = user_service.login_user(login_info=login_info, db=db)
    # server error
    if login_rst.message == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=login_rst.message
        )

    return LoginResponse(
        message=login_rst.message, status_code=status.HTTP_200_OK,
        access_token=login_rst.access_token, refresh_token=login_rst.refresh_token
    )


@user_required_router.post("/refresh")
def get_new_token(
    refresh_body: RefreshRequest,
    jwt_payload: Annotated[JwtPayLoad, Depends(user_service.get_current_user_info)],
    db: Annotated[Session, Depends(get_db_session)]
) -> RefreshResponse:
    if refresh_body.user_id != jwt_payload.user_id:
        raise HTTPException(status_code=401, detail="invalid token")

    get_refresh_rst = user_service.get_new_token(refresh_body=refresh_body, db=db)
    # server error
    if not get_refresh_rst:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error"
        )
    return RefreshResponse(message="success", status_code=status.HTTP_200_OK, access_token=get_refresh_rst[0])

# TODO: 유효한 access token이면 새로운 토큰 발급 x