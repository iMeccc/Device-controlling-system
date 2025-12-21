from fastapi import FastAPI, APIRouter  # <-- 1. Import APIRouter here

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# Import all models to ensure they are registered with SQLAlchemy's metadata
from app.models import user, instrument, reservation, log

# --- Import API Routers ---
from app.api.v1.endpoints import users as users_router
from app.api.v1.endpoints import instruments as instruments_router


def create_tables():
    """
    Creates all database tables defined in the models.
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

    # --- Include API Routers ---
    # Create a single APIRouter to group all v1 endpoints
    api_router = APIRouter()  # <-- 2. Change FastAPI() to APIRouter()
    
    api_router.include_router(users_router.router, prefix="/users", tags=["Users"])
    api_router.include_router(instruments_router.router, prefix="/instruments", tags=["Instruments"])

    # Mount the main v1 router to the app
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
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