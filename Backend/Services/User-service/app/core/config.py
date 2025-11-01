from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "User Service"
    VERSION: str = "1.0.0"

    DB_SERVER: str = "localhost"
    DB_NAME: str = "UrbanTransportDB"
    DB_USER: str = "teste"  # !
    DB_PASSWORD: str = "teste"  # !
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"

    JWT_SECRET: str = "supersecretkey"  # <!!!!!!! alterar mais tarde 31/outubro
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
