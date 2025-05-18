from app.models.submission import Submission, SubmissionStatus
from datetime import datetime
from app.mock_data.constants import TEST_TASK_NAME, TEST_PROMPT_NAME


def parse_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


def submission1():
    return Submission(
        id=1,
        user_id=1,
        prompt=TEST_PROMPT_NAME,
        task_name=TEST_TASK_NAME,
        accuracy=0.5,
        created_at=parse_datetime("2021-01-01 00:00:00"),
        status=SubmissionStatus.completed,
        updated_at=parse_datetime("2021-01-01 00:00:00"),
    )


def submission2():
    # second attempt of user 1, make later than submission1
    return Submission(
        id=2,
        user_id=1,
        prompt=TEST_PROMPT_NAME,
        task_name=TEST_TASK_NAME,
        accuracy=0.6,
        created_at=parse_datetime("2021-01-02 00:00:00"),
        status=SubmissionStatus.completed,
        updated_at=parse_datetime("2021-01-02 00:00:00"),
    )


def submission3():
    return Submission(
        id=3,
        user_id=2,
        prompt=TEST_PROMPT_NAME,
        task_name=TEST_TASK_NAME,
        accuracy=None,
        created_at=parse_datetime("2021-01-01 00:00:00"),
        status=SubmissionStatus.failed,
        updated_at=parse_datetime("2021-01-01 00:00:00"),
    )


def submission4():
    return Submission(
        id=4,
        user_id=3,
        prompt=TEST_PROMPT_NAME,
        task_name=TEST_TASK_NAME,
        accuracy=0.7,
        created_at=parse_datetime("2021-01-01 00:00:00"),
        status=SubmissionStatus.completed,
        updated_at=parse_datetime("2021-01-01 00:00:00"),
    )
