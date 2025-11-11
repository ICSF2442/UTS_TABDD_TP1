# app/core/services/user_service.py
from sqlalchemy.orm import Session
from app.infrastructure.db.user_repository import UserRepository
from app.domain.models.user import User
from app.core.security import hash_password

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
    
    def create_user(self, name: str, email: str, password: str, role: str = "user") -> User:
        if self.repo.find_by_email(email):
            raise ValueError("Email já registado")
        
        if len(password) > 72:
            password = password[:72]
        
        hashed_password = hash_password(password)
        user = User(
            user_id=None,
            name=name,
            email=email,
            password_hash=hashed_password,
            role=role
        )
        
        return self.repo.save(user)
    
    def get_all_users(self) -> list[User]:
        return self.repo.find_all() 
    
    def get_user_by_id(self, user_id: int) -> User:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise ValueError("User não encontrado")
        return user
    
    def update_user(self, user_id: int, name: str = None, email: str = None, password: str = None, role: str = None) -> User:
        user = self.get_user_by_id(user_id)
        
        if email and email != user.email:
            if self.repo.find_by_email(email):
                raise ValueError("Email já está em uso")
            user.email = email
        
        if name:
            user.name = name
        
        if password:
            if len(password) > 72:
                password = password[:72]
            user.password_hash = hash_password(password)
        
        if role:
            user.role = role
        
        return self.repo.update(user)
    
    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        return self.repo.delete(user_id)