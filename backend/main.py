from fastapi import FastAPI

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# Import all models to ensure they are registered with SQLAlchemy's metadata
# before table creation. This is a crucial step.
from app.models import user, instrument, reservation, log

# Import the API router for users
from app.api.v1.endpoints import users as users_router


def create_tables():
    """
    Creates all database tables defined in the models.
    NOTE: In a production environment, this is typically handled by a
    database migration tool like Alembic.
    """
    Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Include the user API router
    app.include_router(users_router.router, prefix=settings.API_V1_STR)
    
    return app


# Create the tables on startup
create_tables()

# Create the FastAPI app instance
app = create_app()


@app.get("/")
def root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API"}