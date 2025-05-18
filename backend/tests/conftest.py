import os
from app.models.submission import Submission
from app.models.user import User
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.core.database import Base
from app.main import app
from fastapi.testclient import TestClient
from app.core.session import get_db
from app.mock_data.users import user1, user2, user3
from app.mock_data.submissions import submission1, submission2, submission3, submission4


@pytest.fixture(scope="session")
def mock_users() -> list[User]:
    return [user1(), user2(), user3()]


@pytest.fixture(scope="session")
def mock_submissions() -> list[Submission]:
    return [submission1(), submission2(), submission3(), submission4()]


@pytest.fixture(scope="session")
def test_db(mock_users, mock_submissions):
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

    # Insert mock users and submissions into the database
    db: Session = TestingSessionLocal()
    try:
        db.add_all(mock_users)
        db.add_all(mock_submissions)
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
