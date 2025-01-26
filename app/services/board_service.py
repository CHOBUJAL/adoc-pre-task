from app.core.utils import get_now_utc
from app.enums.board_enums import BoardAction
from app.enums.common_enums import ResultMessage
from app.models.board_model import Board
from app.repositories import board_repository
from app.schemas.board_schemas import (
    BoardCreateRequest,
    BoardCreateResult,
    BoardDeleteResult,
    BoardGetListResult,
    BoardGetResult,
    BoardListQueryRequest,
    BoardPutRequest,
    BoardPutResult,
)
from app.schemas.user_schemas import (
    JwtPayLoad,
)


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


def get_all_boards(boards_query: BoardListQueryRequest) -> BoardGetListResult:
    all_posts = board_repository.get_all_boards(boards_query=boards_query)
    all_posts.page = boards_query.page
    all_posts.page_size = boards_query.page_size
    return all_posts


def delete_board(post_id: str, jwt_payload: JwtPayLoad) -> BoardDeleteResult:
    post_info = board_repository.get_board(post_id=post_id)
    if post_info.message != ResultMessage.SUCCESS:
        return BoardDeleteResult(message=post_info.message)
    if post_info.post.author_id != jwt_payload.user_id:
        return BoardDeleteResult(message=BoardAction.POST_AUTH_FAIL)

    return board_repository.delete_board(post_id=post_id)


def put_board(
        put_info: BoardPutRequest,
        post_id: str,
        jwt_payload: JwtPayLoad
):
    post_info = board_repository.get_board(post_id=post_id)
    if post_info.message != ResultMessage.SUCCESS:
        return BoardPutResult(message=post_info.message)
    if post_info.post.author_id != jwt_payload.user_id:
        return BoardPutResult(message=BoardAction.POST_AUTH_FAIL)

    return board_repository.put_board(post_body=post_info.post, put_info=put_info)
