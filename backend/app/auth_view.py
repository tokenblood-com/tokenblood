from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.models.user import User

router = APIRouter()


class AuthRequest(BaseModel):
    username: str
    email: str


class AuthResponse(BaseModel):
    status_code: int
    user_id: str | None = None
    error_message: str | None = None


@router.post("/auth", response_model=AuthResponse)
def authenticate_user(auth_data: AuthRequest, db: Session = get_db()):
    existing_user = User.get_by_credentials(db=db, username=auth_data.username, email=auth_data.email)

    if existing_user:
        return AuthResponse(status_code=200, user_id=str(existing_user.id))

    try:
        new_user = User(username=auth_data.username, email=auth_data.email)
        new_user.save(db)
        return AuthResponse(status_code=200, user_id=str(new_user.id))
    except IntegrityError as e:
        db.rollback()
        return _error_message_to_response(str(e.orig))


def _error_message_to_response(error_message: str) -> AuthResponse:
    if "users_username_key" in error_message:
        error_response = AuthResponse(status_code=400, error_message="Username already exists")
    elif "users_email_key" in error_message:
        error_response = AuthResponse(status_code=400, error_message="Email already exists")
    else:
        error_response = AuthResponse(status_code=500, error_message="Internal error")
    return error_response
