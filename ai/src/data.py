from typing import Any
import pandas as pd
from pyrootutils import find_root

import functools
from loguru import logger


@functools.lru_cache()
def load_data(task: str) -> Any:
    if task == "personal_info_extraction":
        data = load_data_for_personal_info_extraction()
    else:
        raise ValueError(f"Task {task} not supported")

    logger.info(f"Task: {task}, dataset size: {len(data)} rows")
    return data


def load_data_for_personal_info_extraction() -> pd.DataFrame:
    """Loads the dataset for the personal info extraction task.

    DATASET_PATH environment variable can be set to the path of the dataset.
    If not set, the dataset will be loaded from the default path.

    Args:
        task (str): Name of the task to load the dataset from SUPPORTED_TASKS

    Returns:
        pd.DataFrame: DataFrame with columns 'inputs' (source text) and 'labels' (list of extracted names)
    """

    dataset_path = find_root() / "data" / "ai4privacy-many-persons-validation.csv"
    logger.info(f"Loaded dataset from {dataset_path}")

    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset not found at {dataset_path.resolve()}")

    data = pd.read_csv(dataset_path, converters={"names": eval})
    data = data.rename(columns={"text": "inputs", "names": "labels"})

    data = data.iloc[:50]

    return data
