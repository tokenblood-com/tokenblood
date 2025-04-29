from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.evaluate import evaluate as _evaluate_fn
from src.metrics import EvaluationResult
from src import SUPPORTED_TASKS


# Define the request body model
class EvaluateRequest(BaseModel):
    task: str
    prompt: str


model_router = APIRouter(tags=["models"], prefix="/models")


@model_router.post("/evaluate", response_model=EvaluationResult)
def evaluate(request: EvaluateRequest):
    """
    Evaluate a given prompt against a specified task dataset.
    """
    if request.task not in SUPPORTED_TASKS:
        raise HTTPException(status_code=400, detail=f"Task {request.task} is not supported")
    # Pass both task and prompt from the request body to the evaluation function
    return _evaluate_fn(task=request.task, prompt=request.prompt)
