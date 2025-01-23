
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.board_schemas import BoardCreateRequest, BoardCreateResponse, BoardGetListResponse
from app.schemas.user_schemas import JwtPayLoad
from app.services import board_service, user_service

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
) -> BoardCreateResponse:
    create_rst = board_service.create_board(create_info=create_info, jwt_payload=jwt_payload)
    if create_rst == "error":
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_rst.message
        )
    return BoardCreateResponse(
        message=create_rst.message, status_code=status.HTTP_200_OK, post_id=create_rst.post_id
    )


@board_router.get("")
def get_all_boards() -> BoardGetListResponse:
    post_list_rst = board_service.get_all_boards()
    if post_list_rst.message == "error":
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=post_list_rst.message
        )
    return BoardGetListResponse(
        message=post_list_rst.message, status_code=status.HTTP_200_OK, post_list=post_list_rst.post_list
    )
