"""请求/响应模型，对照 backend/app/schemas/*.py（那边是 marshmallow，这里是 Pydantic）。

Pydantic 干三件事：
    1. 校验入参：类型不对直接 422，不用手写 if not xxx
    2. 声明出参：response_model 自动裁剪字段（比如永不下发 password_hash）
    3. 生成文档：/docs 里的请求体和响应示例都来自这里
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StoreCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64, description="门店名称")
    address: str = Field(default="", max_length=255)
    phone: str = Field(default="", max_length=32)


class StoreUpdate(BaseModel):
    """全字段可选：只传要改的字段（PATCH 语义）。"""

    name: str | None = Field(default=None, min_length=1, max_length=64)
    address: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=32)
    is_active: bool | None = None


class StoreOut(BaseModel):
    # from_attributes 让 Pydantic 能直接读 ORM 对象的属性
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str
    phone: str
    is_active: bool
    created_at: datetime
