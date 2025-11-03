from app.domain.models.user import User
from sqlalchemy import text

class UserRepository:
    def __init__(self, db):
        self.db = db

    def find_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def find_users_with_favorite(self, line_id: str):
        query = text("""
            SELECT u.user_id, u.name, u.email
            FROM users u
            JOIN favorites f ON u.user_id = f.user_id
            WHERE f.line_id = :line_id
        """)
        result = self.db.execute(query, {"line_id": line_id})
        return result.fetchall()
