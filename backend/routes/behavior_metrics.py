from fastapi import APIRouter, Depends

from core.database import get_db
from core.security import get_current_admin
from models.behavior_metric import BehaviorMetricCRUD
from schemas import BehaviorMetricCreate, BehaviorMetricOut

router = APIRouter(prefix="/behavior-metrics", tags=["behavior-metrics"])


def _as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    import json

    return json.dumps(value, ensure_ascii=False)


@router.get("", response_model=list[BehaviorMetricOut])
@router.get("/", response_model=list[BehaviorMetricOut], include_in_schema=False)
def list_behavior_metrics(
    skip: int = 0,
    limit: int = 100,
    _: dict = Depends(get_current_admin),
):
    with get_db() as conn:
        return BehaviorMetricCRUD.list_all(conn, skip=skip, limit=limit)


@router.get("/summary")
def behavior_summary(_: dict = Depends(get_current_admin)):
    with get_db() as conn:
        return BehaviorMetricCRUD.summary(conn)


@router.post("", response_model=BehaviorMetricOut, status_code=201)
@router.post("/", response_model=BehaviorMetricOut, status_code=201, include_in_schema=False)
def create_behavior_metric(payload: BehaviorMetricCreate):
    data = payload.model_dump()
    # application_id is accepted for compatibility and ignored on purpose.
    data.pop("application_id", None)
    data["time_on_page"] = int(data.get("time_on_page") or data.get("time_on_page_seconds") or 0)
    data["buttons_clicked"] = _as_text(data.get("buttons_clicked"))
    data["cursor_positions"] = _as_text(data.get("cursor_positions"))
    data["return_frequency"] = int(data.get("return_frequency") or 0)
    with get_db() as conn:
        return BehaviorMetricCRUD.create(conn, data)
