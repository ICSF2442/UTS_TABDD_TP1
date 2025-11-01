from sqlalchemy.orm import Session
from app.infrastructure.db.base import UserDB
from app.domain.models.user import User
from app.core.security import hash_password

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: int) -> User | None:
        record = self.db.query(UserDB).filter(UserDB.user_id == user_id).first()
        if not record:
            return None
        return User(
            user_id=record.user_id,
            name=record.name,
            email=record.email,
            password_hash=record.password_hash,
            role=record.role,
            created_at=record.created_at,
        )

    def find_all(self) -> list[User]:
        records = self.db.query(UserDB).all()
        return [
            User(
                user_id=r.user_id,
                name=r.name,
                email=r.email,
                password_hash=r.password_hash,
                role=r.role,
                created_at=r.created_at,
            )
            for r in records
        ]

    def update(self, user: User) -> User:
        db_user = self.db.query(UserDB).filter(UserDB.user_id == user.user_id).first()
        if not db_user:
            return None
        db_user.name = user.name
        db_user.email = user.email
        db_user.password_hash = user.password_hash
        db_user.role = user.role
        self.db.commit()
        self.db.refresh(db_user)
        return user

    def find_by_email(self, email: str) -> User | None:
        record = self.db.query(UserDB).filter(UserDB.email == email).first()
        if not record:
            return None
        return User(
            user_id=record.user_id,
            name=record.name,
            email=record.email,
            password_hash=record.password_hash,
            role=record.role,
            created_at=record.created_at,
        )

    def delete(self, user: User):
        db_user = self.db.query(UserDB).filter(UserDB.user_id == user.user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()

    def save(self, user: User) -> User:
        db_user = UserDB(
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        user.user_id = db_user.user_id
        user.created_at = db_user.created_at
        return user
