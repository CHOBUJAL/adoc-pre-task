from datetime import datetime, timezone

from mongoengine import DateTimeField, Document, IntField, StringField


class Board(Document):
    meta = {
        "collection": "boards",
        "db_alias": "default",
        "indexes": [
            "author_id", "title"
        ]
    }

    author_id = IntField(required=True)
    title = StringField(required=True, max_length=50)
    content = StringField(required=True, max_length=300)
    created_at = DateTimeField(default=lambda: datetime.now(tz=timezone.utc))
    updated_at = DateTimeField()
