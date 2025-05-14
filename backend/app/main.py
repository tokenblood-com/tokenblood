from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.submit import user_router
from app.api.leaderboard import leaderboard_router
from app.core.database import engine
from app.models.user import User
from app.auth_view import router as auth_router

User.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)

# Allow requests from the frontend origin
origins = [
    "http://localhost:5173",  # Vite frontend
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
app.include_router(leaderboard_router, prefix="/api/leaderboard", tags=["leaderboard"])
app.include_router(user_router, prefix="/api/user", tags=["user"])


@app.get("/health")
def healthcheck():
    """
    Healthcheck endpoint to confirm the service is running.
    """
    return {"status": "ok"}
