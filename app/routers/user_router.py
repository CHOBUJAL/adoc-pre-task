from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.schemas.user_schemas import SignUpRequest, SignUpResponse, LoginRequest
from app.services import user_service

user_router = APIRouter(
    prefix="/users",
    tags=["인증이 필요없는 User 관련 라우터"],
)
user_required_router = APIRouter(
    prefix="/users",
    # dependencies=[Depends(get_current_user_info)],
    tags=["인증이 필요한 User 관련 라우터"],
)


@user_router.post("/signup")
def signup_user(
    signup_info: SignUpRequest, db: Annotated[Session, Depends(get_db_session)]
) -> SignUpResponse:
    signup_rst = user_service.signup_user(signup_info=signup_info, db=db)
    
    # db error
    if signup_rst.user is None:
        return SignUpResponse(message=signup_rst.message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # 중복 email
    if signup_rst.message == "already user":
        return SignUpResponse(message=signup_rst.message, status_code=status.HTTP_409_CONFLICT)

    return SignUpResponse(message=signup_rst.message, status_code=status.HTTP_200_OK)


@user_router.post("/login")
def login_user(
    login_info: LoginRequest, db: Annotated[Session, Depends(get_db_session)]
):
    login_rst, a = user_service.login_user(login_info=login_info, db=db)
    return login_rst, a


# @user_router.post("/users/login")
# @user_router.post("/users/refresh")
# @user_router.post("/users/logout")