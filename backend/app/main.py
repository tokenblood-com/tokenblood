from fastapi import FastAPI

from app.core.config import settings
from app.api.model import model_router
from app.core.database import engine
from app.models.user import User
from app.auth_view import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

User.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)

# Allow requests from the frontend origin
origins = [
    "http://localhost:5174",  # Vite frontend
    "https://tokenblood.com",  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api", tags=["auth"])


app.include_router(model_router)


@app.get("/health")
def healthcheck():
    """
    Healthcheck endpoint to confirm the service is running.
    """
    return {"status": "ok"}
