from datetime import datetime

class User:
    def __init__(self, user_id: int, name: str, email: str, password_hash: str, created_at: datetime | None = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<User {self.user_id}: {self.email}>"
