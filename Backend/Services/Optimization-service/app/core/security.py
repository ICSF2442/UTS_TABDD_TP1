from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configuração para hashing de passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------- Password Functions ----------------
def hash_password(password: str) -> str:
    """
    Hash uma password usando bcrypt
    """
    # bcrypt tem limite de 72 bytes, por isso truncamos se necessário
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma password plaintext corresponde ao hash
    """
    # Truncar password se for muito longa (bcrypt limite 72 bytes)
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

# ---------------- JWT Functions ----------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Cria um JWT token de acesso
    """
    to_encode = data.copy()
    
    # Definir expiração
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Codificar JWT
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def verify_access_token(token: str) -> dict | None:
    """
    Verifica e decodifica um JWT token
    Retorna o payload se válido, None se inválido
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None

def get_user_id_from_token(token: str) -> int | None:
    """
    Extrai o user_id de um token JWT
    """
    payload = verify_access_token(token)
    if payload and "user_id" in payload:
        return payload["user_id"]
    return None

def get_user_role_from_token(token: str) -> str | None:
    """
    Extrai a role de um token JWT
    """
    payload = verify_access_token(token)
    if payload and "role" in payload:
        return payload["role"]
    return None