from src.metrics import EvaluationResult


def test_evaluate_api(client):
    debug_task = "personal_info_extraction_debug"
    debug_prompt = """Your task is to extract names from a document. Document can contain one or more names. Output names in the following order: SURNAME (if exists), GIVENNAME (if exists). If document contains multiple names, output all of them with the comma. If document contains no names, output an empty string.

    Here is text of a document:

    {{document}}
    """

    response = client.post(
        "/api/user/submit",
        json={"task": debug_task, "prompt": debug_prompt},
    )

    assert response.status_code == 200

    response_model = EvaluationResult(**response.json())
    assert response_model.accuracy_score > 0.1
