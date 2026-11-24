"""数据访问层：SQL 只出现在这里。

你的 Flask 项目目前是 service 直接写 db.session.query(...)，也能跑；但把查询抽到
repository 的好处是：service 变成纯业务规则，写测试时换掉 repository 就能跑。
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.store import Store


class StoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Store]:
        return list(self.db.scalars(select(Store).order_by(Store.id)).all())

    def get(self, store_id: int) -> Store | None:
        return self.db.get(Store, store_id)

    def get_by_name(self, name: str) -> Store | None:
        return self.db.scalar(select(Store).where(Store.name == name))

    def add(self, store: Store) -> Store:
        self.db.add(store)
        self.db.flush()      # 拿到自增 id，但不提交事务
        return store
