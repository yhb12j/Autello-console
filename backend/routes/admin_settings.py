from fastapi import APIRouter, Depends, HTTPException

from core.database import get_db
from core.security import get_current_admin
from models.admin_setting import AdminSettingCRUD
from schemas import AdminSettingCreate, AdminSettingOut, AdminSettingUpdate

router = APIRouter(prefix="/admin-settings", tags=["admin-settings"])


@router.get("", response_model=list[AdminSettingOut])
@router.get("/", response_model=list[AdminSettingOut], include_in_schema=False)
def list_admin_settings():
    with get_db() as conn:
        return AdminSettingCRUD.list_all(conn)


@router.get("/{item_id}", response_model=AdminSettingOut)
def get_admin_setting(item_id: int):
    with get_db() as conn:
        item = AdminSettingCRUD.get_by_id(conn, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Admin setting not found")
    return item


@router.post("", response_model=AdminSettingOut, status_code=201)
@router.post("/", response_model=AdminSettingOut, status_code=201, include_in_schema=False)
def create_admin_setting(
    payload: AdminSettingCreate,
    _: dict = Depends(get_current_admin),
):
    with get_db() as conn:
        return AdminSettingCRUD.create(conn, payload.model_dump())


@router.put("/{item_id}", response_model=AdminSettingOut)
def update_admin_setting(
    item_id: int,
    payload: AdminSettingUpdate,
    _: dict = Depends(get_current_admin),
):
    with get_db() as conn:
        item = AdminSettingCRUD.update(conn, item_id, payload.model_dump(exclude_unset=True))
    if item is None:
        raise HTTPException(status_code=404, detail="Admin setting not found")
    return item


@router.delete("/{item_id}", status_code=204)
def delete_admin_setting(item_id: int, _: dict = Depends(get_current_admin)):
    with get_db() as conn:
        deleted = AdminSettingCRUD.delete(conn, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Admin setting not found")
