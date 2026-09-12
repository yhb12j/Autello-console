from fastapi import APIRouter, HTTPException

from core.database import get_db
from models.behavior_metric import BehaviorMetricCRUD
from schemas import BehaviorMetricCreate, BehaviorMetricOut

router = APIRouter(prefix="/behavior-metrics", tags=["behavior-metrics"])


@router.get("", response_model=list[BehaviorMetricOut])
def list_behavior_metrics():
    with get_db() as conn:
        return BehaviorMetricCRUD.list_all(conn)


@router.get("/{item_id}", response_model=BehaviorMetricOut)
def get_behavior_metric(item_id: int):
    with get_db() as conn:
        item = BehaviorMetricCRUD.get_by_id(conn, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Behavior metric not found")
    return item


@router.post("", response_model=BehaviorMetricOut, status_code=201)
def create_behavior_metric(payload: BehaviorMetricCreate):
    with get_db() as conn:
        return BehaviorMetricCRUD.create(conn, payload.model_dump())


@router.delete("/{item_id}", status_code=204)
def delete_behavior_metric(item_id: int):
    with get_db() as conn:
        deleted = BehaviorMetricCRUD.delete(conn, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Behavior metric not found")
