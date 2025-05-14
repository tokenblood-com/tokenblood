import json
import os
from app.models.submission import Submission
from app.models.user import User
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import Base
from pyrootutils import find_root
from app.main import app
from fastapi.testclient import TestClient
from app.core.session import get_db


@pytest.fixture(scope="session")
def test_users() -> list[User]:
    data_path = find_root() / "tests" / "test_data" / "users.json"
    with open(data_path, "r") as f:
        users = json.load(f)

    users = [User(**user) for user in users]
    return users


@pytest.fixture(scope="session")
def test_submissions() -> list[Submission]:
    data_path = find_root() / "tests" / "test_data" / "submissions.json"
    with open(data_path, "r") as f:
        submissions = json.load(f)

    for submission in submissions:
        submission["created_at"] = datetime.strptime(submission["created_at"], "%Y-%m-%d %H:%M:%S")
        submission["updated_at"] = datetime.strptime(submission["updated_at"], "%Y-%m-%d %H:%M:%S")

    submissions = [Submission(**submission) for submission in submissions]
    return submissions


@pytest.fixture(scope="session")
def test_db(test_users, test_submissions):
    test_db_url = "sqlite:///./test.db"
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Insert test users and submissions into the database
    db: Session = TestingSessionLocal()
    try:
        db.add_all(test_users)
        db.add_all(test_submissions)
        db.commit()
    finally:
        db.close()

    yield db

    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client
