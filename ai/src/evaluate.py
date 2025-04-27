import pandas as pd

from dotenv import load_dotenv

from src import SUPPORTED_TASKS
from src.data import load_data
from src.llm_infer import run_prompt
from src.metrics import EvaluationResult, calculate_metrics

load_dotenv()


def evaluate(task: str, prompt: str, debug: bool = False) -> EvaluationResult:
    if task not in SUPPORTED_TASKS:
        raise ValueError(f"Task {task} not supported, supported tasks are: {SUPPORTED_TASKS}")

    data: pd.DataFrame = load_data(task)
    predictions: pd.DataFrame = run_prompt(prompt, data)
    metrics: EvaluationResult = calculate_metrics(task, predictions, debug)

    return metrics
