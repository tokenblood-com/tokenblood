from sqlalchemy.orm import Session


class CRUDMixin:
    """Allows to run .save() on models, e.g. for User model"""

    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
