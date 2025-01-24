from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.enums.board_enums import BoardAction, BoardOrderType
from app.exceptions.board_exception import board_exception_handler


class BasePageSchema(BaseModel):
    page: int = Field(default=1, min=1)
    page_size: int = Field(default=10, min=5, max=50)

    @model_validator(mode="before")
    def validate_page_and_size(cls, values):
        page = values.get("page", 1)
        page_size = values.get("page_size", 10)

        if page < 1:
            board_exception_handler(detail=BoardAction.INVALID_PAGE)
        if not 5 <= page_size <= 50:
            board_exception_handler(detail=BoardAction.INVALID_PAGE_SIZE)

        return values


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


class BoardListQueryRequest(BasePageSchema):
    user_id: int | None = None
    title: str | None = None
    order_type: BoardOrderType = BoardOrderType.CREATE_AT_LATEST

class BoardGetListResult(BasePageSchema):
    message: str
    post_list: list[BoardBody] = []
    total_count: int | None = None


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
