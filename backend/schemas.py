from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AdminSettingCreate(BaseModel):
    services: str = Field(..., min_length=1, max_length=240)
    budget_range: str = Field(..., min_length=1, max_length=120)


class AdminSettingUpdate(BaseModel):
    services: str | None = Field(default=None, min_length=1, max_length=240)
    budget_range: str | None = Field(default=None, min_length=1, max_length=120)


class AdminSettingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    services: str
    budget_range: str
    created_at: str
    updated_at: str


class BehaviorPayload(BaseModel):
    time_on_page_seconds: int = 0
    buttons_clicked: list[Any] = Field(default_factory=list)
    hover_zones: list[Any] = Field(default_factory=list)
    return_count: int = 1
    extra_payload: dict[str, Any] = Field(default_factory=dict)


class ApplicationCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=120)
    last_name: str = Field(..., min_length=1, max_length=120)
    patronymic: str = ""
    phone: str = Field(..., min_length=5, max_length=64)
    email: str = Field(..., min_length=5, max_length=180)
    business_info: str = ""
    business_niche: str = ""
    company_size: str = ""
    business_size: str = ""
    role: str = ""
    task_volume: str = ""
    need_volume: str = ""
    deadline: str = ""
    task_type: str = ""
    product: str = ""
    budget: str = ""
    contact_method: str = ""
    convenient_time: str = ""
    comment: str = ""
    behavior: BehaviorPayload | None = None


class ApplicationUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    phone: str | None = None
    email: str | None = None
    business_info: str | None = None
    business_niche: str | None = None
    company_size: str | None = None
    business_size: str | None = None
    role: str | None = None
    task_volume: str | None = None
    need_volume: str | None = None
    deadline: str | None = None
    task_type: str | None = None
    product: str | None = None
    budget: str | None = None
    contact_method: str | None = None
    convenient_time: str | None = None
    comment: str | None = None


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str
    business_info: str
    business_niche: str
    company_size: str
    business_size: str
    role: str
    task_volume: str
    need_volume: str
    deadline: str
    task_type: str
    product: str
    budget: str
    contact_method: str
    convenient_time: str
    comment: str
    created_at: str


class BehaviorMetricCreate(BaseModel):
    application_id: int
    time_on_page_seconds: int = 0
    buttons_clicked: list[Any] = Field(default_factory=list)
    hover_zones: list[Any] = Field(default_factory=list)
    return_count: int = 1
    extra_payload: dict[str, Any] = Field(default_factory=dict)


class BehaviorMetricOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    time_on_page_seconds: int
    buttons_clicked: list[Any]
    hover_zones: list[Any]
    return_count: int
    extra_payload: dict[str, Any]
    created_at: str
