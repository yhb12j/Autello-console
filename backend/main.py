from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import init_tables, wait_for_db
from routes import admin_settings_router, applications_router, auth_router, behavior_metrics_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    wait_for_db()
    init_tables()
    yield


app = FastAPI(
    title="Autéllo Barskiy API",
    description="Private intake contour for atelier requests, metrics and operator console.",
    version="1.1.0",
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_settings_router)
app.include_router(applications_router)
app.include_router(behavior_metrics_router)


@app.get("/health")
def health():
    return {"status": "ok"}
