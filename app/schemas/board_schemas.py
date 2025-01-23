from datetime import datetime

from pydantic import BaseModel, ConfigDict



class BoardCreateRequest(BaseModel):
    title: str
    content: str

class BoardCreateResponse(BaseModel):
    message: str
    status_code: int
    post_id: str

class BoardGetResponse(BaseModel):
    post_id: str
    author_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
