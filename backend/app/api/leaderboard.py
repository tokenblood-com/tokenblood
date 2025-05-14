from app.models.submission import Submission
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.session import get_db
from src import SUPPORTED_TASKS

leaderboard_router = APIRouter()


@leaderboard_router.get("/")
def get_leaderboard(task_name: str, db: Session = Depends(get_db)):
    if task_name not in SUPPORTED_TASKS:
        raise HTTPException(status_code=400, detail=f"Task {task_name} is not supported")
    leaderboard = Submission.get_leaderboard_for_task(db, task_name)
    return leaderboard
