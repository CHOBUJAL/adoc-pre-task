from app.models.board_model import Board
from app.schemas.board_schemas import BoardCreateResult, BoardGetListResult, BoardGetResult


def create_board(new_post: Board) -> BoardCreateResult:
    try:
        new_post.save()
    except Exception:
        return BoardCreateResult(message="error")
    return BoardCreateResult(message="success", post_id=str(new_post.id))


def get_all_boards() -> BoardGetListResult:
    try:
        all_posts = [
            BoardGetResult(
                post_id=str(post.id),
                author_id=post.author_id,
                title=post.title,
                content=post.content,
                created_at=post.created_at,
                updated_at=post.updated_at,
            ) for post in Board.objects()
        ]
    except Exception as e:
        print(e)
        return BoardGetListResult(message="error")

    return BoardGetListResult(message="success", post_list=all_posts)
