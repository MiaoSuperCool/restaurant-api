"""第一个模型：门店。对照 backend/app/models/store.py。

注意这里没有 import 任何 web 框架 —— 模型是纯 SQLAlchemy，可以脱离 FastAPI 使用。
"""
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class Store(BaseModel):
    __tablename__ = "stores"

    name: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    phone: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
