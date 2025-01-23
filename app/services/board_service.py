from app.models.board_model import Board
from app.repositories import board_repository
from app.schemas.board_schemas import (
    BoardCreateRequest,
    BoardCreateResult,
    BoardDeleteResult,
    BoardGetListResult,
    BoardGetResult,
)
from app.schemas.user_schemas import (
    JwtPayLoad,
)
from app.core.utils import get_now_utc


def create_board(
        create_info: BoardCreateRequest, jwt_payload: JwtPayLoad
) -> BoardCreateResult:
    new_post = Board(
        author_id=jwt_payload.user_id,
        title=create_info.title,
        content=create_info.content,
        created_at=get_now_utc()
    )

    return board_repository.create_board(new_post)

def get_board(post_id: str) -> BoardGetResult:
    post = board_repository.get_board(post_id=post_id)
    return post

def get_all_boards() -> BoardGetListResult:
    all_posts = board_repository.get_all_boards()
    return all_posts


# def delete_board(post_id: str, jwt_payload: JwtPayLoad) -> BoardDeleteResult:
#     return board_repository.delete_board(post_id=post_id, jwt_payload=jwt_payload)
