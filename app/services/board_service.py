from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from app.schemas.board_schemas import BoardCreateRequest, BoardCreateResponse, BoardGetResponse
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.schemas.user_schemas import (
    JwtPayLoad,
    LoginRequest,
    LoginResult,
    LogoutRequest,
    LogoutResult,
    RefreshRequest,
    SignUpRequest,
    SignupResult,
)
from app.settings import settings
from app.models.board_model import Board
from app.repositories import board_repository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_now_utc():
    return datetime.now(tz=timezone.utc)
# 평문을 해시값으로
def create_board(create_info: BoardCreateRequest, jwt_payload: JwtPayLoad) -> BoardCreateResponse:
    new_post = Board(
        author_id=jwt_payload.user_id,
        title=create_info.title,
        content=create_info.content,
        created_at=get_now_utc
    )

    create_rst = board_repository.create_board(new_post)
    return BoardCreateResponse(
        message="success",
        status_code=status.HTTP_200_OK,
        post_id=str(create_rst.id)
    )


# def get_all_boards() -> BoardGetResponse:
#     all_boards = board_repository.get_all_boards()
#     return board_repository.get_all_boards()