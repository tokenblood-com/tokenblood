from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine
from app.models.user import User
from app.auth_view import router as auth_router

User.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)

app.include_router(auth_router, prefix="/api/", tags=["auth"])


@app.get("/health")
def healthcheck():
    """
    Healthcheck endpoint to confirm the service is running.
    """
    return {"status": "ok"}
