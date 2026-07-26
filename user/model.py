from database.orm import Base
from datetime import datetime
from sqlalchemy import  Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"
    id = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    email: Mapped[str] = mapped_column(
        String(256), unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

