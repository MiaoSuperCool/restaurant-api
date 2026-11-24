# FastAPI 重写练手项目：restaurant-api

把 Flask 版餐厅后端（restaurant-system）按同样的分层、同样的模块顺序，用 FastAPI 重写一遍。
阶段 0 / 1 已搭好并验证通过，阶段 2 的门店模块是**参考实现**，接下来的模块由你自己写。

## 快速开始

```powershell
cd D:\DearCodes\Python\FastAPIProjects\restaurant-api
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

打开 http://127.0.0.1:8000/docs ，直接在页面上调 `GET /api/v1/stores`。

跑测试：

```powershell
pytest
```

## 分层与来源

```text
app/
  main.py                    应用入口 + 全局异常处理    ← backend/app/__init__.py
  core/config.py             配置                        ← app/config.py
  core/errors.py             领域异常                    ← app/errors.py
  core/response.py           统一响应信封                ← app/utils/api_response.py
  db/base.py                 ORM 基类                    ← app/models/base.py
  db/session.py              引擎与会话依赖              ← app/extensions.py
  models/store.py            模型                        ← app/models/store.py
  schemas/store.py           Pydantic 出入参             ← app/schemas/*.py（marshmallow）
  repositories/store_repo.py 数据访问                    ← 你项目里是 service 直接查库
  services/store_service.py  业务层                      ← app/services/*.py
  api/deps.py                依赖注入                    ← flask.g / current_user
  api/v1/*.py                路由                        ← app/api/*.py（Blueprint）
tests/                       pytest                      ← backend/tests/*.py
docs/学习路线.md              八个阶段 + 练习 + 验收标准
```

## 下一步

按 [学习路线](docs/学习路线.md) 走。当前该做的是**阶段 2 的练习**：

1. 读 `app/api/v1/stores.py` 和 `app/services/store_service.py`，搞清楚谁负责 commit、404 是谁抛的。
2. **不看 store 代码**，自己写 `categories` 模块（列表、新增、改名、停用）+ 4 个测试。
3. 把 `main.py` 里的 `create_all` 换成 Alembic 迁移。

写完发出来，按两条挑毛病：路由里不许有 SQL，service 里不许出现 `fastapi`。

## 约定

1. `service` 只 raise `AppError` 家族的异常，不认识 HTTP。
2. 事务边界在 service，不在 router，也不在 `get_db`。
3. 路由函数只做三件事：收参数、调 service、包响应。
