"""业务层：对照 backend/app/services/store_service.py。

三条规矩，做到这三条才算「业务与框架解耦」：
    1. 不 import fastapi / starlette / flask
    2. 不收 Request 对象，也不读全局登录态（用户从参数传进来）
    3. 写操作在这里 commit —— 事务边界 = 用例边界，不是 HTTP 请求边界
"""
from sqlalchemy.orm import Session

from app.core.errors import ConflictError, NotFoundError
from app.models.store import Store
from app.repositories.store_repo import StoreRepository
from app.schemas.store import StoreCreate, StoreUpdate


class StoreService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = StoreRepository(db)

    def list_stores(self) -> list[Store]:
        return self.repo.list_all()

    def get_store(self, store_id: int) -> Store:
        store = self.repo.get(store_id)
        if store is None:
            raise NotFoundError(f"门店 {store_id} 不存在")
        return store

    def create_store(self, payload: StoreCreate) -> Store:
        if self.repo.get_by_name(payload.name) is not None:
            raise ConflictError("同名门店已存在")

        store = Store(**payload.model_dump())
        self.repo.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store

    def update_store(self, store_id: int, payload: StoreUpdate) -> Store:
        store = self.get_store(store_id)

        # exclude_unset：只更新客户端真正传了的字段
        changes = payload.model_dump(exclude_unset=True)
        if "name" in changes:
            same_name = self.repo.get_by_name(changes["name"])
            if same_name is not None and same_name.id != store_id:
                raise ConflictError("同名门店已存在")

        for field, value in changes.items():
            setattr(store, field, value)

        self.db.commit()
        self.db.refresh(store)
        return store

    def delete_store(self, store_id: int) -> None:
        store = self.get_store(store_id)
        self.db.delete(store)
        self.db.commit()
