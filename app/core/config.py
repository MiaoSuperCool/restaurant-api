"""配置：用 pydantic-settings 替代你 Flask 项目里的 DevelopmentConfig / ProductionConfig。

Flask 的做法：
    class DevelopmentConfig(Config): ...

FastAPI 的做法：
    一个 Settings 类，字段来自环境变量 / .env 文件，类型不对启动就报错。
    好处是「配置错了当场炸」，而不是跑到某个接口里才发现。
"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# parents[2] = fastapi-learning/（本文件在 app/core/config.py）
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # 这样 .env 里写 ENV=dev，就会自动映射到 self.env
        case_sensitive=False,
    )

    app_name: str = "FastAPI 学习项目"
    env: str = "dev"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # 默认 SQLite，零依赖即可跑通。换 PostgreSQL 时只改环境变量。
    database_url: str = f"sqlite:///{(BASE_DIR / 'data' / 'dev.db').as_posix()}"


# 全局单例：任何地方 from app.core.config import settings 即可
settings = Settings()
