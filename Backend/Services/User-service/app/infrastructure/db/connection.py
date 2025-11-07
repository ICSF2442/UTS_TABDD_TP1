from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import urllib.parse

# Connection string
encoded_password = urllib.parse.quote_plus(settings.DB_PASSWORD)
DATABASE_URL = (
    f"mssql+pyodbc://{settings.DB_USER}:{encoded_password}@"
    f"{settings.DB_SERVER}/{settings.DB_NAME}?"
    f"driver={urllib.parse.quote_plus(settings.DB_DRIVER)}&"
    f"TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()