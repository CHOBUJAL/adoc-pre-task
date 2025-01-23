from datetime import datetime, timezone

from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from app.models.board_model import Board
from app.repositories import board_repository
from app.schemas.board_schemas import (
    BoardCreateRequest,
    BoardCreateResult,
    BoardGetListResult,
)
from app.schemas.user_schemas import (
    JwtPayLoad,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_now_utc():
    return datetime.now(tz=timezone.utc)
# 평문을 해시값으로
def create_board(create_info: BoardCreateRequest, jwt_payload: JwtPayLoad) -> BoardCreateResult:
    new_post = Board(
        author_id=jwt_payload.user_id,
        title=create_info.title,
        content=create_info.content,
        created_at=get_now_utc
    )

    return board_repository.create_board(new_post)


def get_all_boards() -> BoardGetListResult:
    all_boards = board_repository.get_all_boards()
    return all_boards
