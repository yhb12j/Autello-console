from fastapi import APIRouter, Depends, HTTPException

from core.database import get_db
from core.scoring import score_application
from core.security import get_current_admin
from models.application import ApplicationCRUD
from schemas import ApplicationCreate, ApplicationOut, ApplicationQueueItem, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=list[ApplicationOut])
@router.get("/", response_model=list[ApplicationOut], include_in_schema=False)
def list_applications(
    skip: int = 0,
    limit: int = 100,
    _: dict = Depends(get_current_admin),
):
    with get_db() as conn:
        items = ApplicationCRUD.list_all(conn)
    return items[skip : skip + limit]


@router.get("/queue", response_model=list[ApplicationQueueItem])
def list_application_queue(_: dict = Depends(get_current_admin)):
    with get_db() as conn:
        items = ApplicationCRUD.list_all(conn)
    ranked = [score_application(item) for item in items]
    heat = {"hot": 0, "warm": 1, "cold": 2}
    ranked.sort(key=lambda item: (heat[item["temperature"]], -item["score"], item["id"]))
    return ranked


@router.get("/{item_id}", response_model=ApplicationQueueItem)
def get_application(item_id: int, _: dict = Depends(get_current_admin)):
    with get_db() as conn:
        item = ApplicationCRUD.get_by_id(conn, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return score_application(item)


@router.post("", response_model=ApplicationOut, status_code=201)
@router.post("/", response_model=ApplicationOut, status_code=201, include_in_schema=False)
def create_application(payload: ApplicationCreate):
    data = payload.model_dump(exclude={"behavior"})
    with get_db() as conn:
        return ApplicationCRUD.create(conn, data)


@router.put("/{item_id}", response_model=ApplicationOut)
def update_application(
    item_id: int,
    payload: ApplicationUpdate,
    _: dict = Depends(get_current_admin),
):
    with get_db() as conn:
        item = ApplicationCRUD.update(conn, item_id, payload.model_dump(exclude_unset=True))
    if item is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return item


@router.delete("/{item_id}", status_code=204)
def delete_application(item_id: int, _: dict = Depends(get_current_admin)):
    with get_db() as conn:
        deleted = ApplicationCRUD.delete(conn, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
