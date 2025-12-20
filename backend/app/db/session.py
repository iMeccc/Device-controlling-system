from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

db_url = settings.SQLALCHEMY_DATABASE_URI
if db_url is None:
	raise RuntimeError("SQLALCHEMY_DATABASE_URI must be set in settings")

engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    FastAPI dependency that provides a database session for each request.
    It ensures that the database session is always closed after the request is finished,
    even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()