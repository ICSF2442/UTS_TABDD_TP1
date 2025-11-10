from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    VERSION: str

    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()