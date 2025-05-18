from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from app.core.database import Base
from app.models.crud_mixin import CRUDMixin
from sqlalchemy import func
from sqlalchemy import Enum as SQLAlchemyEnum
import enum


class SubmissionStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Submission(Base, CRUDMixin):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prompt = Column(String)
    task = Column(String)
    accuracy = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    status = Column(SQLAlchemyEnum(SubmissionStatus))
    updated_at = Column(DateTime, default=datetime.now())
    error_message = Column(String, nullable=True)

    @classmethod
    def get_leaderboard_for_task(cls, db: Session, task: str):
        """Generate a leaderboard for all users sorted by their accuracy for a specific task.

        If user has multiple submissions, only the highest accuracy submission is returned.
        """

        # Step 1: Create a subquery to rank submissions for each user.
        # Submissions are partitioned by user_id and ordered by accuracy (descending)
        # and then by creation_date (descending, as a tie-breaker).
        # Only submissions with non-null accuracy are considered.
        ranked_submissions_sq = (
            db.query(
                cls.id,  # Select the primary key of the submission for joining
                func.row_number()
                .over(partition_by=cls.user_id, order_by=[cls.accuracy.desc(), cls.created_at.desc()])
                .label("rank_submission"),  # Assign a rank (row number)
            )
            .filter(cls.accuracy.isnot(None))
            .subquery("ranked_submissions")
        )

        # Step 2: Query the main Submission table.
        # Join with the subquery to get the rank for each submission.
        # Filter to keep only the top-ranked submission (rn = 1) for each user.
        # Order the final result by accuracy in descending order to form the leaderboard.
        leaderboard = (
            db.query(cls)
            .filter(cls.task == task)
            .filter(cls.status == SubmissionStatus.completed)
            .join(
                ranked_submissions_sq,
                cls.id == ranked_submissions_sq.c.id,  # Join on the submission ID
            )
            .filter(
                ranked_submissions_sq.c.rank_submission == 1  # Select only the best submission per user
            )
            .order_by(
                cls.accuracy.desc()  # Order the leaderboard by accuracy
            )
            .all()
        )

        return leaderboard

    @classmethod
    def get_user_submissions_for_task(cls, db: Session, user_id: int, task: str):
        """Get all submissions for a user for a specific task."""
        return db.query(cls).filter(cls.user_id == user_id, cls.task == task).order_by(cls.created_at.desc()).all()
