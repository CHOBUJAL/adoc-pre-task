from bson import ObjectId
from mongoengine.errors import DoesNotExist

from app.core.utils import get_now_utc
from app.enums.board_enums import BoardAction
from app.enums.common_enums import ResultMessage
from app.models.board_model import Board
from app.schemas.board_schemas import (
    BoardBody,
    BoardCreateResult,
    BoardDeleteResult,
    BoardGetListResult,
    BoardGetResult,
    BoardListQueryRequest,
    BoardPutRequest,
    BoardPutResult,
)


def create_board(new_post: Board) -> BoardCreateResult:
    try:
        new_post.save()
    except Exception:
        return BoardCreateResult(message=ResultMessage.ERROR)
    return BoardCreateResult(message=ResultMessage.SUCCESS, post_id=str(new_post.id))


def get_all_boards(boards_query: BoardListQueryRequest) -> BoardGetListResult:
    try:
        # 게시글 필터
        filter_boards = Board.objects()
        if boards_query.user_id:
            filter_boards = filter_boards.filter(author_id=boards_query.user_id)
        if boards_query.title:
            # 대소문자 구분 x
            filter_boards = filter_boards.filter(title__regex=f"(?i){boards_query.title}")

        # 게시글 정렬
        filter_boards = filter_boards.order_by(boards_query.order_type)

         # 페이지네이션
        total_count = filter_boards.count()
        skip = (boards_query.page - 1) * boards_query.page_size  # 건너뛸 문서 수
        filter_boards = filter_boards.skip(skip).limit(boards_query.page_size)  # 페이지네이션 적용

        all_posts = [
            BoardBody(
                post_id=str(post.id),
                author_id=post.author_id,
                title=post.title,
                content=post.content,
                created_at=post.created_at,
                updated_at=post.updated_at,
            ) for post in filter_boards
        ]
    except Exception as e:
        print(e)
        return BoardGetListResult(message=ResultMessage.ERROR)

    return BoardGetListResult(
        message=ResultMessage.SUCCESS,
        post_list=all_posts,
        total_count=total_count
    )


def get_board(post_id: str) -> BoardGetResult:
    try:
        post = Board.objects.get(id=ObjectId(post_id))
    except DoesNotExist:
        return BoardGetResult(message=BoardAction.NO_POST_FOUND)
    except Exception:
        return BoardGetResult(message=ResultMessage.ERROR)
    return BoardGetResult(
        message=ResultMessage.SUCCESS,
        post=BoardBody(
            post_id=str(post.id),
            author_id=post.author_id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
    )

def delete_board(post_id: str) -> BoardDeleteResult:
    try:
        post = Board.objects.get(id=ObjectId(post_id))
        post.delete()
    except Exception:
        return BoardDeleteResult(message=ResultMessage.ERROR)
    return BoardDeleteResult(message=ResultMessage.SUCCESS, post_id=post_id)


def put_board(post_body: BoardBody, put_info: BoardPutRequest) -> BoardPutResult:
    try:
        put_post = Board.objects.get(id=ObjectId(post_body.post_id))
        if put_info.title:
            put_post.title = put_info.title
        if put_info.content:
            put_post.content = put_info.content
        if put_info.title or put_info.content:
            put_post.updated_at = get_now_utc()
        put_post.save()
    except Exception:
        return BoardPutResult(message=ResultMessage.ERROR)
    return BoardPutResult(message=ResultMessage.SUCCESS, post_id=str(put_post.id))
