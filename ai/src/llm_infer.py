import os

from openai import OpenAI
import pandas as pd


MODEL_NAME = os.environ["OPENAI_MODEL_NAME"]

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def run_prompt(prompt: str, inputs: pd.DataFrame) -> pd.DataFrame:
    if prompt.count("{{document}}") != 1:
        raise ValueError("Prompt must contain exactly one {{document}} placeholder")

    outputs = []

    for _, row in inputs.iterrows():
        prompt_with_document = prompt.replace("{{document}}", row["inputs"])

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt_with_document}],
        )

        model_output = response.choices[0].message.content

        outputs.append(model_output)

    inputs["outputs"] = outputs

    return inputs
