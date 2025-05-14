from app.models.user import User
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.evaluate import evaluate as _evaluate_fn
from src.metrics import EvaluationResult
from src import SUPPORTED_TASKS
from app.models.submission import Submission
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.session import get_db


class EvaluateRequest(BaseModel):
    task: str
    prompt: str


user_router = APIRouter()


@user_router.post("/submit", response_model=EvaluationResult)
def submit(request: EvaluateRequest):
    """
    Evaluate a given prompt against a specified task dataset.
    """
    if request.task not in SUPPORTED_TASKS:
        raise HTTPException(status_code=400, detail=f"Task {request.task} is not supported")

    return _evaluate_fn(task=request.task, prompt=request.prompt)


@user_router.get("/submissions")
def get_user_submissions(user_id: int, task_name: str, db: Session = Depends(get_db)):
    if task_name not in SUPPORTED_TASKS:
        raise HTTPException(status_code=400, detail=f"Task {task_name} is not supported")

    if user_id not in [user.id for user in db.query(User.id).all()]:
        raise HTTPException(status_code=400, detail=f"User {user_id} does not exist")

    submissions = Submission.get_user_submissions_for_task(db, user_id, task_name)
    return submissions
