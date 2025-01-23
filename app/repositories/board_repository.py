from bson import ObjectId

from app.enums.enum import ResultMessage
from app.models.board_model import Board
from app.schemas.board_schemas import (
    BoardBody,
    BoardCreateResult,
    BoardGetListResult,
    BoardGetResult,
)


def create_board(new_post: Board) -> BoardCreateResult:
    try:
        new_post.save()
    except Exception:
        return BoardCreateResult(message=ResultMessage.ERROR)
    return BoardCreateResult(message=ResultMessage.SUCCESS, post_id=str(new_post.id))


def get_all_boards() -> BoardGetListResult:
    try:
        all_posts = [
            BoardBody(
                post_id=str(post.id),
                author_id=post.author_id,
                title=post.title,
                content=post.content,
                created_at=post.created_at,
                updated_at=post.updated_at,
            ) for post in Board.objects()
        ]
    except Exception:
        return BoardGetListResult(message=ResultMessage.ERROR)

    return BoardGetListResult(message=ResultMessage.SUCCESS, post_list=all_posts)


def get_board(post_id: str) -> BoardGetResult:
    try:
        post = Board.objects.get(id=ObjectId(post_id))
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
