from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "User Service"
    VERSION: str = "1.0.0"
    JWT_SECRET: str = "supersecretkey"  # <!!!!!!! alterar mais tarde 31/outubro
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
