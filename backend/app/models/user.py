from sqlalchemy import Column, String, Integer
from app.core.database import Base
from sqlalchemy.orm import Session
from app.models.crud_mixin import CRUDMixin


class User(Base, CRUDMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    @classmethod
    def get_by_credentials(cls, db: Session, username: str, email: str) -> "User | None":
        return db.query(cls).filter(cls.username == username, cls.email == email).first()
