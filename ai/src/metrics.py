from pydantic import BaseModel
import pandas as pd


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


def calculate_metrics_personal_info_extraction(pred_df: pd.DataFrame, debug: bool = False):
    gt_names: list[list[str]] = pred_df["labels"].tolist()
    predictions: list[list[str]] = [p.split(", ") for p in pred_df["outputs"].tolist()]

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for i, (prediction, gt_name) in enumerate(zip(predictions, gt_names)):
        true_positives += len([p for p in prediction if p in gt_name])
        false_positives += len([p for p in prediction if p not in gt_name])
        false_negatives = len([n for n in gt_name if n not in prediction])

        if debug:
            print(f"Index: {i}")
            print(f"- prediction: {prediction}")
            print(f"- gt_name: {gt_name}")
            print()

    accuracy_score = true_positives / (true_positives + false_positives + false_negatives)

    return EvaluationResult(
        accuracy_score=accuracy_score,
        true_positives=true_positives,
        false_positives=false_positives,
        false_negatives=false_negatives,
        dataset_size=len(pred_df),
    )


def calculate_metrics(task: str, predictions: pd.DataFrame, debug: bool = False) -> EvaluationResult:
    if "personal_info_extraction" in task:
        return calculate_metrics_personal_info_extraction(predictions, debug)
    else:
        raise ValueError(f"Task {task} not supported")
