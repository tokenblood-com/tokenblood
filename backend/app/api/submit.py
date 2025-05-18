from datetime import datetime
from app.models.user import User
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.evaluate import evaluate as _evaluate_fn
from src import SUPPORTED_TASKS
from app.models.submission import Submission, SubmissionStatus
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.session import get_db
from loguru import logger


class EvaluateRequest(BaseModel):
    user_id: int
    task: str
    prompt: str


user_router = APIRouter()


@user_router.post("/submit")
def submit(request: EvaluateRequest, db: Session = Depends(get_db)):
    """
    Evaluate a given prompt against a specified task dataset.
    """
    if request.task not in SUPPORTED_TASKS:
        raise HTTPException(status_code=400, detail=f"Task {request.task} is not supported")

    created_at = datetime.now()

    try:
        eval_result = _evaluate_fn(task=request.task, prompt=request.prompt)
        logger.success(f"Evaluation result for user {request.user_id} on task {request.task}: {eval_result}")

        submission = Submission(
            user_id=request.user_id,
            prompt=request.prompt,
            task=request.task,
            accuracy=eval_result.accuracy_score,
            created_at=created_at,
            status=SubmissionStatus.completed,
            updated_at=datetime.now(),
        )
        submission.save(db)
        return {
            "submission_id": submission.id,
            "accuracy_score": eval_result.accuracy_score,
            "status": SubmissionStatus.completed,
            "error_message": None,
        }

    except Exception as e:
        logger.error(f"Error evaluating prompt: {e}")
        submission = Submission(
            user_id=request.user_id,
            prompt=request.prompt,
            task=request.task,
            accuracy=None,
            created_at=created_at,
            status=SubmissionStatus.failed,
            error_message=str(e),
        )
        submission.save(db)

        return {
            "submission_id": submission.id,
            "accuracy_score": None,
            "status": SubmissionStatus.failed,
            "error_message": str(e),
        }


@user_router.get("/submissions")
def get_user_submissions(user_id: int, task: str, db: Session = Depends(get_db)):
    if task not in SUPPORTED_TASKS:
        raise HTTPException(status_code=400, detail=f"Task {task} is not supported")

    if user_id not in [user.id for user in db.query(User.id).all()]:
        raise HTTPException(status_code=400, detail=f"User {user_id} does not exist")

    submissions = Submission.get_user_submissions_for_task(db, user_id, task)
    return submissions
