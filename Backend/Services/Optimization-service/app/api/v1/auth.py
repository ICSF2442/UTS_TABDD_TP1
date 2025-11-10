from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_access_token

# Scheme para Bearer token
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency para obter o utilizador atual a partir do token JWT
    """
    token = credentials.credentials
    payload = verify_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=401, 
            detail="Token de acesso inválido ou expirado"
        )
    
    return payload

def require_role(required_role: str):
    """
    Dependency para verificar se o utilizador tem uma role específica
    """
    def role_dependency(current_user = Depends(get_current_user)):
        user_role = current_user.get("role")
        
        if user_role != required_role:
            raise HTTPException(
                status_code=403, 
                detail=f"Acesso negado. Role necessária: {required_role}"
            )
        
        return current_user
    
    return role_dependency

def optional_auth(credentials: HTTPAuthorizationCredentials | None = Depends(security)):
    """
    Dependency opcional - retorna user se autenticado, None se não
    """
    if credentials:
        token = credentials.credentials
        payload = verify_access_token(token)
        return payload
    return None