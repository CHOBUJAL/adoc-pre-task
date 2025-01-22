from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session, get_mongo_conn
from app.models.board_model import Board

board_router = APIRouter(
    prefix="/boards",
    tags=["인증이 필요없는 게시판 관련 라우터"],
)
# user_required_router = APIRouter(
#     prefix="/users",
#     dependencies=[Depends(user_service.get_current_user_info)],
#     tags=["인증이 필요한 User 관련 라우터"],
# )


"""
id = StringField(primary_key=True)  # _id
    author_id = IntField(required=True)  # 저자 id (user_id)
    title = StringField(required=True, max_length=100)  # 제목
    content = StringField(required=True)  # 내용
    created_at = DateTimeField(default=lambda: datetime.now(tz=timezone.utc))  # 생성시간
    updated_at = DateTimeField()  # 수정시간"""
@board_router.post("")
def test():
    b = Board(
        author_id=100,
        title="test",
        content="kasdnaeskj213123"
    )
    b.save()
    return [{"123": a.content, "11": a.id} for a in Board.objects()]
