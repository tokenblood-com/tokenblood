import os
from pathlib import Path
from typing import Any
import pandas as pd

import functools
from loguru import logger
import socket

from pyrootutils import find_root


if "tokenblood-vm" in socket.gethostname():
    DATASET_DIR = Path("/data")  # dataset location on google cloud vm
else:
    DATASET_DIR = find_root().parent / "data"  # dataset location for local development


IS_GITHUB_ACTIONS = "GITHUB_ACTIONS" in os.environ


@functools.lru_cache()
def load_data(task: str) -> Any:
    if task == "personal_info_extraction":
        data = load_data_for_personal_info_extraction(num_rows=50)
    elif task == "personal_info_extraction_debug":
        data = load_data_for_personal_info_extraction(num_rows=3)
    else:
        raise ValueError(f"Task {task} not supported")

    logger.info(f"Task: {task}, dataset size: {len(data)} rows")
    return data


def load_data_for_personal_info_extraction(num_rows: int = 50) -> pd.DataFrame:
    """Loads the dataset for the personal info extraction task.

    DATASET_PATH environment variable can be set to the path of the dataset.
    If not set, the dataset will be loaded from the default path.

    Args:
        task (str): Name of the task to load the dataset from SUPPORTED_TASKS

    Returns:
        pd.DataFrame: DataFrame with columns 'inputs' (source text) and 'labels' (list of extracted names)
    """
    if IS_GITHUB_ACTIONS:
        logger.info("Running in GitHub Actions, using debug dataset")
        ai_dir = find_root().parent / "ai"
        dataset_path = ai_dir / "tests" / "test_data" / "personal_info_extraction_debug.csv"
    else:
        dataset_path = DATASET_DIR / "personal_info_extraction" / "ai4privacy" / "v1" / "eval.csv"

    logger.info(f"Loaded dataset from {dataset_path}")

    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset not found at {dataset_path.resolve()}")

    data = pd.read_csv(dataset_path, converters={"names": eval})
    data = data.rename(columns={"text": "inputs", "names": "labels"})

    data = data.iloc[:num_rows]

    return data
