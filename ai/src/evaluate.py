from pydantic import BaseModel
import pandas as pd

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

MODEL_NAME = os.environ["OPENAI_MODEL_NAME"]

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


class EvaluationResult(BaseModel):
    """
    Evaluation result for a model.
    Args:
        accuracy_score: float - accuracy score of the model
        true_positives: int - number of correct model predictions
        false_positives: int - number of incorrect model predictions
        false_negatives: int - number of missing model predictions
        dataset_size: int - size of the dataset
    """

    accuracy_score: float
    true_positives: int
    false_positives: int
    false_negatives: int
    dataset_size: int


def calculate_metrics(predictions: list[str], names: list[str]):
    true_positives = len([p for p in predictions if p in names])
    false_positives = len([p for p in predictions if p not in names])
    false_negatives = len([n for n in names if n not in predictions])

    return true_positives, false_positives, false_negatives


def evaluate_model(prompt: str, evaluation_df: pd.DataFrame, verbose: bool = False) -> EvaluationResult:
    if prompt.count("{{document}}") != 1:
        raise ValueError("Prompt must contain exactly one {{document}} placeholder")

    if verbose:
        print(f"Evaluating model on {len(evaluation_df)} samples with prompt")
        print(prompt)

    results = []

    for index, row in evaluation_df.iterrows():
        text = row["text"]
        gt_names = row["names"]

        prompt_with_document = prompt.replace("{{document}}", text)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt_with_document}],
        )

        model_output = response.choices[0].message.content
        pred_names = model_output.split(", ")

        results.append(calculate_metrics(pred_names, gt_names))

        if verbose:
            print(f"Index: {index}")
            print(f"- text: {pred_names}")
            print(f"- gt_names: {gt_names}")
            print()

    tp = sum([result[0] for result in results])
    fp = sum([result[1] for result in results])
    fn = sum([result[2] for result in results])
    dataset_size = len(results)

    accuracy_score = tp / (tp + fp + fn)

    return EvaluationResult(
        accuracy_score=accuracy_score,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        dataset_size=dataset_size,
    )
