from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.infrastructure.db.connection import get_db
from app.infrastructure.db.user_repository import UserRepository
from app.core.security import verify_password, create_access_token, verify_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

security_scheme = HTTPBearer()

@router.post("/login")
def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    try:
        repo = UserRepository(db)
        user = repo.find_by_email(email)
        
        if not user:
            raise HTTPException(status_code=401, detail="Email ou password incorretos")
        
        # Truncar password se for muito longa
        if len(password) > 72:
            password = password[:72]
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Email ou password incorretos")

        # Criar token JWT com dados REAIS do user
        token_data = {
            "sub": user.email, 
            "user_id": user.user_id, 
            "role": user.role
        }
        access_token = create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no login: {str(e)}")

# Dependency para obter usuário atual a partir do token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        repo = UserRepository(db)
        user = repo.find_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erro de autenticação: {str(e)}")

# Dependency para verificar role
def require_role(required_role: str):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="Permissão insuficiente")
        return current_user
    return role_checker