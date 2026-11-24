"""健康检查。对照 backend/app/api/main.py。

写 async 还是 def，判断标准只有一条：
    函数体里有没有阻塞调用（数据库、Redis、HTTP、文件）？
    有 → 用 def，FastAPI 丢线程池执行，不堵事件循环。
    没有 → 用 async def。
这里的 /health 只读内存，所以 async 没问题。
"""
from fastapi import APIRouter

from app.core.config import settings
from app.core.response import ApiResponse, ok

router = APIRouter(tags=["系统"])


@router.get("/health", response_model=ApiResponse[dict], summary="健康检查")
async def health() -> ApiResponse[dict]:
    return ok({"status": "ok", "env": settings.env})
