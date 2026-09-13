from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AdminRegister(BaseModel):
    login: str = Field(..., min_length=3, max_length=80)
    password: str = Field(..., min_length=6, max_length=128)
    email: EmailStr | None = None


class AdminLogin(BaseModel):
    login: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminOut(BaseModel):
    id: int
    login: str
    email: str | None = None
    created_at: str


class AuthCheckOut(BaseModel):
    exists: bool


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
    behavior: dict[str, Any] | None = None


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


class ApplicationQueueItem(ApplicationOut):
    score: int
    temperature: str
    temperature_label: str
    need_manager: bool
    department: str
    analysis: str


class BehaviorMetricCreate(BaseModel):
    application_id: int | None = 0
    time_on_page: int = 0
    buttons_clicked: Any = ""
    cursor_positions: Any = ""
    return_frequency: int = 0
    time_on_page_seconds: int | None = None
    hover_zones: Any = None
    extra_payload: Any = None


class BehaviorMetricOut(BaseModel):
    id: int
    time_on_page: int
    buttons_clicked: str
    cursor_positions: str
    return_frequency: int
    created_at: str
