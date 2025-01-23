
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user_info
from app.enums.common_enums import ResultMessage
from app.schemas.board_schemas import (
    BoardCreateRequest,
    BoardCreateResponse,
    BoardGetListResponse,
    BoardGetResponse,
)
from app.schemas.user_schemas import JwtPayLoad
from app.services import board_service

board_router = APIRouter(
    prefix="/boards",
    tags=["인증이 필요없는 게시판 관련 라우터"],
)
board_required_router = APIRouter(
    prefix="/boards",
    dependencies=[Depends(get_current_user_info)],
    tags=["인증이 필요한 게시판 관련 라우터"],
)


@board_required_router.post("")
def create_board(
    create_info: BoardCreateRequest,
    jwt_payload: Annotated[JwtPayLoad, Depends(get_current_user_info)]
) -> BoardCreateResponse:
    create_rst = board_service.create_board(create_info=create_info, jwt_payload=jwt_payload)
    if create_rst == ResultMessage.ERROR:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_rst.message
        )
    return BoardCreateResponse(
        message=create_rst.message, status_code=status.HTTP_200_OK, post_id=create_rst.post_id
    )


@board_router.get("")
def get_all_boards() -> BoardGetListResponse:
    post_list_rst = board_service.get_all_boards()
    if post_list_rst.message == ResultMessage.ERROR:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=post_list_rst.message
        )
    return BoardGetListResponse(
        message=post_list_rst.message, status_code=status.HTTP_200_OK, post_list=post_list_rst.post_list
    )


@board_router.get("/{post_id}")
def get_board(post_id: str) -> BoardGetResponse:
    post_rst = board_service.get_board(post_id=post_id)
    if post_rst.message == ResultMessage.ERROR:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=post_rst.message
        )

    return BoardGetResponse(
        message=post_rst.message, status_code=status.HTTP_200_OK, post=post_rst.post
    )


@board_required_router.put("/{post_id}")
def put_board(
    
)
# @board_required_router.delete()