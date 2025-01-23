from datetime import datetime

from pydantic import BaseModel


class BoardCreateRequest(BaseModel):
    title: str
    content: str

class BoardCreateResult(BaseModel):
    message: str
    post_id: str | None = None

class BoardCreateResponse(BoardCreateResult):
    status_code: int


class BoardGetResult(BaseModel):
    post_id: str
    author_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime | None


class BoardGetListResult(BaseModel):
    message: str
    post_list: list[BoardGetResult] = []


class BoardGetListResponse(BoardGetListResult):
    status_code: int
