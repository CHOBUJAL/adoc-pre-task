
from datetime import datetime, timezone
from typing import Any, Dict, List
from fastapi import status

from sqlalchemy import select, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from app.models.user_model import RefreshTokenOrm, UserOrm
from app.schemas.user_schemas import (
    LoginResult,
    LogoutRequest,
    LogoutResult,
    RefreshRequest,
    SignupResult,
)
from app.models.board_model import Board

def create_board(new_post: Board) -> Board:
    try:
        new_post.save()
        print(type(new_post))
    except Exception:
        raise Exception
    return new_post

# def get_all_boards():
    