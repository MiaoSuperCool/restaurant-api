"""统一响应信封，对照你的 backend/app/utils/api_response.py。

区别在于：这里用 Pydantic 泛型声明的，不是拼 dict。
    - 响应结构在 /docs 里能直接看到
    - response_model= 会做一次校验和裁剪，多返回的字段自动丢掉
    - 前端可以据此生成 TypeScript 类型
"""
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    code: str = "ok"
    message: str = ""
    data: T | None = None


def ok(data: T | None = None, message: str = "操作成功", code: str = "ok") -> ApiResponse[T]:
    return ApiResponse[T](success=True, code=code, message=message, data=data)


def fail(message: str, code: str = "error") -> ApiResponse[None]:
    return ApiResponse[None](success=False, code=code, message=message, data=None)
