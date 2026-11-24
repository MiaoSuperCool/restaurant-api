"""数据库连接与会话，对照 backend/app/extensions.py 里 db = SQLAlchemy() 那部分。

Flask 用 db.init_app(app) 把扩展绑到应用上，会话由框架按请求管理。
FastAPI 没有这套绑定：引擎是普通对象，会话通过 Depends 注入，请求结束自动 close。
"""
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# SQLite 需要先建目录，否则 create_engine 连接时才报错
if settings.database_url.startswith("sqlite:///"):
    Path(settings.database_url.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)

# SQLite 在 FastAPI 的线程池里被多线程访问，必须关掉同线程检查
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(
    settings.database_url,
    echo=settings.debug,          # 开发期打印 SQL，生产关掉
    connect_args=connect_args,
    pool_pre_ping=True,           # 连接失效自动重连，线上必备
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """请求级会话。用 yield 依赖，FastAPI 会在请求结束后执行 finally。

    注意：这里不做 commit。事务边界由 service 的用例决定（见 store_service）。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
