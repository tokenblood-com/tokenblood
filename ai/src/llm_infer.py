import os
import concurrent.futures

from openai import OpenAI
import pandas as pd
from loguru import logger

MODEL_NAME = os.environ["OPENAI_MODEL_NAME"]

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def run_prompt(prompt: str, inputs: pd.DataFrame, max_workers: int = 10) -> pd.DataFrame:
    """Runs the given prompt for each input document in the DataFrame using multithreading.

    Be aware that the function will raise an error if openai api returns an error on any of the documents.

    Args:
        prompt: The prompt template string. Must contain "{{document}}".
        inputs: DataFrame with an "inputs" column containing the documents.

    Returns:
        The input DataFrame with an added "outputs" column containing the model responses.

    Raises:
        ValueError: If the prompt does not contain exactly one "{{document}}" placeholder.
    """
    if prompt.count("{{document}}") != 1:
        raise ValueError("Prompt must contain exactly one {{document}} placeholder")

    def _get_openai_response(input_document: str) -> str:
        """Helper function to call OpenAI API for a single document.

        Args:
            input_document: The input document to process.

        Returns:
            The model output for the input document.
        """
        prompt_with_document = prompt.replace("{{document}}", input_document)
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt_with_document}],
            )
            model_output = response.choices[0].message.content
            return model_output if model_output is not None else ""
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise ValueError(f"Error processing document: {e}, input: {input_document}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(_get_openai_response, inputs["inputs"]))

    inputs["outputs"] = results
    return inputs
