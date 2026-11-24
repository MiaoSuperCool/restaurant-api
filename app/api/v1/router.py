"""v1 路由总装。对照 backend/app/__init__.py 里 register_blueprint 的那一段。

以后每加一个模块，只改这个文件一行 —— 这就是「模块化」的落点。
"""
from fastapi import APIRouter

from app.api.v1 import health, stores

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(stores.router)
