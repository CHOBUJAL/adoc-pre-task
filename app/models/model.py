import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from zoneinfo import ZoneInfo


class Base(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        default=lambda: datetime.datetime.now(ZoneInfo("UTC")),
        comment="레코드가 생성된 시간 in UTC",
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        index=True,
        default=None,
        onupdate=lambda: datetime.datetime.now(ZoneInfo("UTC")),
        comment="레코드가 마지막으로 업데이트된 시간 in UTC",
    )
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), index=True, default=None, comment="레코드가 지워진 시간 in UTC"
    )