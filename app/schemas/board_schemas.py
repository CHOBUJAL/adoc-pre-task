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


class BoardBody(BaseModel):
    post_id: str
    author_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime | None


class BoardGetListResult(BaseModel):
    message: str
    post_list: list[BoardBody] = []


class BoardGetListResponse(BoardGetListResult):
    status_code: int


class BoardGetResult(BaseModel):
    message: str
    post: BoardBody | None = None


class BoardGetResponse(BoardGetResult):
    status_code: int


class BoardDeleteResult(BoardCreateResult):
    pass
class BoardDeleteResponse(BoardCreateResponse):
    pass

class BoardPutRequest(BoardCreateRequest):
    title: str | None = None
    content: str | None = None

class BoardPutResult(BoardCreateResult):
    pass
