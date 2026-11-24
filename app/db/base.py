"""ORM 基类，对照 backend/app/models/base.py。

Flask-SQLAlchemy 用 db.Model / db.Column；SQLAlchemy 2.0 原生用 DeclarativeBase + Mapped。
后者是「裸 SQLAlchemy」，不绑定任何框架——FastAPI、CLI 脚本、Celery worker 都能用。
"""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """所有模型的根。alembic 靠它拿 metadata。"""


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )
