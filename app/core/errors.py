"""领域异常：业务代码只认识这些，不认识 HTTP。

对照你的 Flask 项目 backend/app/errors.py —— 思路完全一样，只是多带了一个
机器可读的 code 字段，方便客户端（Flutter / Vue）按 code 分支，而不是去比中文文案。

关键约束（这是「业务与框架解耦」的核心）：
    service 层只 raise 这里的异常，绝不 import fastapi。
    异常 → HTTP 状态码的转换，统一在 main.py 的 exception_handler 里做。
"""


class AppError(Exception):
    """所有可预期业务错误的基类。"""

    status_code: int = 400
    code: str = "business_error"

    def __init__(self, message: str, *, status_code: int | None = None, code: str | None = None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"


class UnauthorizedError(AppError):
    status_code = 401
    code = "unauthorized"


class ForbiddenError(AppError):
    status_code = 403
    code = "forbidden"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"


class ValidationError(AppError):
    status_code = 422
    code = "validation_error"
