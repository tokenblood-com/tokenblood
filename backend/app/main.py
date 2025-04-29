from fastapi import FastAPI

from app.core.config import settings
from app.api.model import model_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)


app.include_router(model_router)


@app.get("/health")
def healthcheck():
    """
    Healthcheck endpoint to confirm the service is running.
    """
    return {"status": "ok"}
