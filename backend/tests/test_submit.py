from app.models.submission import Submission
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

TEST_TASK_NAME = "personal_info_extraction_debug"


def test_leaderboard_db(test_db: Session):
    leaderboard = Submission.get_leaderboard_for_task(
        test_db,
        task_name=TEST_TASK_NAME,
    )
    leaderboard = sorted(leaderboard, key=lambda x: x.user_id)

    # from user "1" we have 2 submissions with accuracy 0.5 and 0.6, should be only one in leaderboard
    # from user "3" we have only one submission with accuracy 0.7
    # from user "2" we have failed submission
    assert len(leaderboard) == 2
    assert leaderboard[0].user_id == 1
    assert leaderboard[1].user_id == 3
    assert leaderboard[0].accuracy == 0.6
    assert leaderboard[1].accuracy == 0.7

    user_attempts = Submission.get_user_submissions_for_task(test_db, user_id=1, task_name=TEST_TASK_NAME)
    assert len(user_attempts) == 2
    assert user_attempts[0].accuracy == 0.5
    assert user_attempts[1].accuracy == 0.6


def test_leaderboard_api(client: TestClient):
    response = client.get("/api/leaderboard", params={"task_name": TEST_TASK_NAME})

    assert response.status_code == 200, response.json()
    response_data = response.json()
    assert len(response_data) == 2

    response_data = sorted(response_data, key=lambda x: x["user_id"])
    assert response_data[0]["user_id"] == 1
    assert response_data[1]["user_id"] == 3
    assert response_data[0]["accuracy"] == 0.6
    assert response_data[1]["accuracy"] == 0.7


def test_user_submissions_api(client: TestClient):
    response = client.get("/api/user/submissions", params={"user_id": 1, "task_name": TEST_TASK_NAME})
    assert response.status_code == 200, response.json()

    response_data = response.json()
    assert len(response_data) == 2

    response_data = sorted(response_data, key=lambda x: x["accuracy"])
    assert response_data[0]["accuracy"] == 0.5
    assert response_data[1]["accuracy"] == 0.6
