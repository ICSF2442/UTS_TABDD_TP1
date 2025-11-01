from sqlalchemy.orm import Session
from app.infrastructure.db.base import FeedbackDB


class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_feedback(self, user_id: int, rating: int, comments: str | None):
        feedback = FeedbackDB(user_id=user_id, rating=rating, comments=comments)
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def get_feedback_by_user(self, user_id: int):
        return self.db.query(FeedbackDB).filter(FeedbackDB.user_id == user_id).all()

    def get_all_feedback(self):
        return self.db.query(FeedbackDB).all()
