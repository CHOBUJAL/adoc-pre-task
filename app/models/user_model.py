from app.models.model import Base

from sqlalchemy.orm import Mapped, mapped_column

class UserOrm(Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "사용자 정보"}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(comment="사용자 이름")
    phone_number: Mapped[str] = mapped_column(comment="사용자 전화번호")
    email: Mapped[str] = mapped_column(comment="사용자 이메일")
    hashed_password: Mapped[str] = mapped_column(comment="사용자 비밀번호")
    address: Mapped[str] = mapped_column(comment="사용자 주소", default="test")
