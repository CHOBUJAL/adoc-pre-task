
from typing import Annotated
from app.schemas.board_schemas import BoardCreateRequest
from app.schemas.user_schemas import JwtPayLoad
from fastapi import APIRouter, Depends

from app.models.board_model import Board
from app.services import user_service, board_service

board_router = APIRouter(
    prefix="/boards",
    tags=["인증이 필요없는 게시판 관련 라우터"],
)
board_required_router = APIRouter(
    prefix="/boards",
    dependencies=[Depends(user_service.get_current_user_info)],
    tags=["인증이 필요한 게시판 관련 라우터"],
)


@board_required_router.post("")
def create_board(
    create_info: BoardCreateRequest,
    jwt_payload: Annotated[JwtPayLoad, Depends(user_service.get_current_user_info)]
):
    return board_service.create_board(create_info=create_info, jwt_payload=jwt_payload)


# @board_router.get("")
# def get_all_boards():
#     return board_service.get_all_boards()
