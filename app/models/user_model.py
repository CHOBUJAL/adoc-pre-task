import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.model import Base

DEFAULT_STRING_LENGTH = 255

class UserOrm(Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "사용자 정보"}

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(DEFAULT_STRING_LENGTH), comment="사용자 이메일")
    hashed_password: Mapped[str] = mapped_column(String(DEFAULT_STRING_LENGTH), comment="사용자 비밀번호")

class RefreshTokenOrm(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = {"comment": "사용자 refresh token 정보"}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        comment="user pk", index=True, unique=True
    )
    refresh_token: Mapped[str] = mapped_column(
        String(DEFAULT_STRING_LENGTH), nullable=True, comment="사용자 refresh token"
    )

    # 관계 정의 (users 테이블과 연결)
    user: Mapped[UserOrm] = relationship(UserOrm)
