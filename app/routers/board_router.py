
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user_info
from app.enums.board_enums import BoardAction
from app.enums.common_enums import ResultMessage
from app.exceptions.board_exception import board_exception_handler
from app.schemas.board_schemas import (
    BoardCreateRequest,
    BoardCreateResponse,
    BoardDeleteResponse,
    BoardGetListResponse,
    BoardGetResponse,
    BoardPutRequest,
)
from app.schemas.user_schemas import JwtPayLoad
from app.services import board_service


def validate_post_id(post_id: str) -> str:
    try:
        return str(ObjectId(post_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=BoardAction.INVALID_ID_FORMAT
        )

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
    if create_rst != ResultMessage.SUCCESS:
        board_exception_handler(detail=create_rst)
    return BoardCreateResponse(
        message=create_rst.message, status_code=status.HTTP_200_OK, post_id=create_rst.post_id
    )


@board_router.get("")
def get_all_boards() -> BoardGetListResponse:
    post_list_rst = board_service.get_all_boards()
    if post_list_rst.message != ResultMessage.SUCCESS:
        board_exception_handler(detail=post_list_rst.message)
    return BoardGetListResponse(
        message=post_list_rst.message, status_code=status.HTTP_200_OK, post_list=post_list_rst.post_list
    )


@board_router.get("/{post_id}")
def get_board(post_id: Annotated[str, Depends(validate_post_id)]) -> BoardGetResponse:
    post_rst = board_service.get_board(post_id=post_id)
    if post_rst.message != ResultMessage.SUCCESS:
        board_exception_handler(detail=post_rst.message)
    return BoardGetResponse(
        message=post_rst.message, status_code=status.HTTP_200_OK, post=post_rst.post
    )


@board_required_router.delete("/{post_id}")
def delete_board(
    post_id: Annotated[str, Depends(validate_post_id)],
    jwt_payload: Annotated[JwtPayLoad, Depends(get_current_user_info)]
) -> BoardDeleteResponse:
    delete_rst = board_service.delete_board(post_id=post_id, jwt_payload=jwt_payload)
    if delete_rst.message != ResultMessage.SUCCESS:
        board_exception_handler(detail=delete_rst.message)
    return BoardDeleteResponse(
        message=delete_rst.message, status_code=status.HTTP_200_OK, post_id=delete_rst.post_id
    )

@board_required_router.put("/{post_id}")
def put_board(
    put_info: BoardPutRequest,
    post_id: Annotated[str, Depends(validate_post_id)],
    jwt_payload: Annotated[JwtPayLoad, Depends(get_current_user_info)]
):
    put_rst = board_service.put_board(
        put_info=put_info, post_id=post_id, jwt_payload=jwt_payload
    )
    if put_rst.message != ResultMessage.SUCCESS:
        board_exception_handler(detail=put_rst.message)
    return BoardDeleteResponse(
        message=put_rst.message, status_code=status.HTTP_200_OK, post_id=put_rst.post_id
    )
