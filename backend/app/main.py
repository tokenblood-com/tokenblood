from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)


@app.get("/health")
def healthcheck():
    """
    Healthcheck endpoint to confirm the service is running.
    """
    return {"status": "ok"}
