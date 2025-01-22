from datetime import datetime, timezone
from mongoengine import Document, StringField, DateTimeField, IntField


class Board(Document):
    meta = {
        "collection": "boards",
        "db_alias": "default",
        "indexes": [
            "author_id"
        ]
    }

    author_id = IntField(required=True)  # 저자 id (user_id)
    title = StringField(required=True, max_length=50)  # 제목
    content = StringField(required=True, max_length=300)  # 내용
    created_at = DateTimeField(default=lambda: datetime.now(tz=timezone.utc))  # 생성시간
    updated_at = DateTimeField()  # 수정시간
