from datetime import datetime

class User:
    def __init__(self, user_id, name, email, password_hash, role, created_at=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<User {self.user_id}: {self.email} ({self.role})>"