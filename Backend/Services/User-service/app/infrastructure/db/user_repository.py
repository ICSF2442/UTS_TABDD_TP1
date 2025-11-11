from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.infrastructure.db.models.user_db import UserDB
from app.domain.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, db_user: UserDB) -> User:
        if not db_user:
            return None
        return User(
            user_id=db_user.user_id,
            name=db_user.name,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role=db_user.role,
            created_at=db_user.created_at,
        )

    def find_by_id(self, user_id: int) -> User | None:
        record = self.db.query(UserDB).filter(UserDB.user_id == user_id).first()
        return self._to_domain(record)

    def find_by_email(self, email: str) -> User | None:
        record = self.db.query(UserDB).filter(UserDB.email == email).first()
        return self._to_domain(record)

    def find_all(self) -> list[User]:
        records = self.db.query(UserDB).all()  
        return [self._to_domain(record) for record in records]

    def save(self, user: User) -> User:
        try:
            db_user = UserDB(
                name=user.name,
                email=user.email,
                password_hash=user.password_hash,
                role=user.role,
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_domain(db_user)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Email já existe")
        except Exception as e:
            self.db.rollback()
            raise

    def update(self, user: User) -> User:
        try:
            db_user = self.db.query(UserDB).filter(UserDB.user_id == user.user_id).first()
            if not db_user:
                raise ValueError("User não encontrado")
            
            db_user.name = user.name
            db_user.email = user.email
            db_user.password_hash = user.password_hash
            db_user.role = user.role
            
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_domain(db_user)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Email já existe")
        except Exception as e:
            self.db.rollback()
            raise

    def delete(self, user_id: int) -> bool:
        try:
            db_user = self.db.query(UserDB).filter(UserDB.user_id == user_id).first()
            if not db_user:
                raise ValueError("User não encontrado")
            
            self.db.delete(db_user)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise