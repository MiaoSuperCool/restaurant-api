"""依赖注入：FastAPI 替代 flask.g / current_user 的地方。

后面阶段 3 会在这里加 get_current_user、require_permission。
现在只有数据库会话。
"""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

DbSession = Annotated[Session, Depends(get_db)]
