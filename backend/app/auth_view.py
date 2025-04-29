import logging
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.session import get_db
from app.models.user import User

router = APIRouter()


class AuthRequest(BaseModel):
    username: str
    email: str


@router.post("/auth")
def authenticate_user(auth_data: AuthRequest, db: Session = Depends(get_db)):
    existing_user = User.get_by_credentials(db=db, username=auth_data.username, email=auth_data.email)
    if existing_user:
        return {"user_id": str(existing_user.id)}
    try:
        new_user = User(username=auth_data.username, email=auth_data.email)
        new_user.save(db)
        return {"user_id": str(new_user.id)}
    except IntegrityError as e:
        db.rollback()
        _raise_http_exception(str(e.orig))


def _raise_http_exception(error_message: str):
    if "UNIQUE constraint failed: users.email" in error_message:
        raise HTTPException(status_code=400, detail="Username already exists")
    elif "UNIQUE constraint failed: users.username" in error_message:
        raise HTTPException(status_code=400, detail="Email already exists")
    else:
        logging.error(f"Internal error: {error_message}")
        raise HTTPException(status_code=500, detail="Internal error")
