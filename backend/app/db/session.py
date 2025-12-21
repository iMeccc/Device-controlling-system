from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

db_url = settings.SQLALCHEMY_DATABASE_URI
if db_url is None:
    raise RuntimeError("SQLALCHEMY_DATABASE_URI must be set in settings")

"""
This is the crucial change. The 'connect_args' dictionary is passed
directly to the underlying database driver (psycopg2), forcing it
to use 'utf8' for the client encoding at the lowest connection level.
"""

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    connect_args={"client_encoding": "utf8"}
)

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