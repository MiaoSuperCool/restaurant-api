"""应用入口。对照 backend/app/__init__.py 的 create_app()。

FastAPI 里没有「应用工厂」的硬性要求，但保留工厂函数是对的：
测试要用不同配置建实例，直接模块级 app = FastAPI() 会把自己写死。
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import models  # noqa: F401  导入模型，让 Base.metadata 认识所有表
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.errors import AppError
from app.core.response import fail
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 开发期用 create_all 快速起步；阶段 1 的练习是换成 alembic 迁移。
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",          # 自动生成的交互式文档
        redoc_url="/redoc",
    )

    # ---------- 全局异常处理：领域异常 → HTTP ----------
    # 这一步是「service 不认识 fastapi」的前提。
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content=fail(exc.message, code=exc.code).model_dump(),
        )

    # 参数校验失败（Pydantic）也统一成同一套信封，前端不用写两套解析
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        first = exc.errors()[0] if exc.errors() else {}
        msg = f"参数不合法：{'.'.join(str(x) for x in first.get('loc', []))} {first.get('msg', '')}"
        return JSONResponse(
            status_code=422,
            content=fail(msg.strip(), code="validation_error").model_dump(),
        )

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
