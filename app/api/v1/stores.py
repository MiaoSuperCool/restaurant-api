"""门店接口。对照 backend/app/api/stores.py（flask-smorest Blueprint）。

路由函数的职责只有三件：接收参数 → 调 service → 包成响应。
业务判断、SQL、commit 都不该出现在这里。
"""
from fastapi import APIRouter, status

from app.api.deps import DbSession
from app.core.response import ApiResponse, ok
from app.schemas.store import StoreCreate, StoreOut, StoreUpdate
from app.services.store_service import StoreService

router = APIRouter(prefix="/stores", tags=["门店"])


@router.get("", response_model=ApiResponse[list[StoreOut]], summary="门店列表")
def list_stores(db: DbSession) -> ApiResponse[list[StoreOut]]:
    stores = StoreService(db).list_stores()
    return ok([StoreOut.model_validate(s) for s in stores])


@router.get("/{store_id}", response_model=ApiResponse[StoreOut], summary="门店详情")
def get_store(store_id: int, db: DbSession) -> ApiResponse[StoreOut]:
    store = StoreService(db).get_store(store_id)
    return ok(StoreOut.model_validate(store))


@router.post(
    "",
    response_model=ApiResponse[StoreOut],
    status_code=status.HTTP_201_CREATED,
    summary="新增门店",
)
def create_store(payload: StoreCreate, db: DbSession) -> ApiResponse[StoreOut]:
    store = StoreService(db).create_store(payload)
    return ok(StoreOut.model_validate(store), message="创建成功")


@router.patch("/{store_id}", response_model=ApiResponse[StoreOut], summary="修改门店")
def update_store(store_id: int, payload: StoreUpdate, db: DbSession) -> ApiResponse[StoreOut]:
    store = StoreService(db).update_store(store_id, payload)
    return ok(StoreOut.model_validate(store), message="更新成功")


@router.delete("/{store_id}", response_model=ApiResponse[None], summary="删除门店")
def delete_store(store_id: int, db: DbSession) -> ApiResponse[None]:
    StoreService(db).delete_store(store_id)
    return ok(None, message="删除成功")
