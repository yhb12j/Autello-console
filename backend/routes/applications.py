from fastapi import APIRouter, HTTPException

from core.database import get_db
from models.application import ApplicationCRUD
from models.behavior_metric import BehaviorMetricCRUD
from schemas import ApplicationCreate, ApplicationOut, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=list[ApplicationOut])
@router.get("/", response_model=list[ApplicationOut], include_in_schema=False)
def list_applications():
    with get_db() as conn:
        return ApplicationCRUD.list_all(conn)


@router.get("/{item_id}", response_model=ApplicationOut)
def get_application(item_id: int):
    with get_db() as conn:
        item = ApplicationCRUD.get_by_id(conn, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return item


@router.post("", response_model=ApplicationOut, status_code=201)
@router.post("/", response_model=ApplicationOut, status_code=201, include_in_schema=False)
def create_application(payload: ApplicationCreate):
    data = payload.model_dump(exclude={"behavior"})
    with get_db() as conn:
        application = ApplicationCRUD.create(conn, data)
        if payload.behavior is not None:
            BehaviorMetricCRUD.create(
                conn,
                {
                    "application_id": application["id"],
                    **payload.behavior.model_dump(),
                },
            )
        return application


@router.put("/{item_id}", response_model=ApplicationOut)
def update_application(item_id: int, payload: ApplicationUpdate):
    with get_db() as conn:
        item = ApplicationCRUD.update(conn, item_id, payload.model_dump(exclude_unset=True))
    if item is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return item


@router.delete("/{item_id}", status_code=204)
def delete_application(item_id: int):
    with get_db() as conn:
        deleted = ApplicationCRUD.delete(conn, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
