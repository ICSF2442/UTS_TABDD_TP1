from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Connection string for local SQL Server
DATABASE_URL = (
    f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_SERVER}/{settings.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


