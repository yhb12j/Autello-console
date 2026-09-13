from .admin_settings import router as admin_settings_router
from .applications import router as applications_router
from .auth import router as auth_router
from .behavior_metrics import router as behavior_metrics_router

__all__ = [
    "admin_settings_router",
    "applications_router",
    "auth_router",
    "behavior_metrics_router",
]
