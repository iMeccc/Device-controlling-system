from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# --- 1. CRUCIAL: Import ALL models so create_all knows about them ---
from app.models import user, instrument, reservation, log, permission

# --- Import API Routers ---
from app.api.v1.endpoints import users as users_router
from app.api.v1.endpoints import instruments as instruments_router
from app.api.v1.endpoints import reservations as reservations_router
from app.api.v1.endpoints import permissions as permissions_router

def create_tables():
    """
    Creates all database tables defined in the imported models.
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

    # --- Add the CORS middleware ---
    origins = [
        "http://localhost:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # --- Include API Routers ---
    api_router = APIRouter()
    
    # --- 2. CRUCIAL: Add ALL routers to api_router BEFORE mounting it ---
    api_router.include_router(users_router.router, prefix="/users", tags=["Users"])
    api_router.include_router(instruments_router.router, prefix="/instruments", tags=["Instruments"])
    api_router.include_router(reservations_router.router, prefix="/reservations", tags=["Reservations"])
    api_router.include_router(permissions_router.router, prefix="/permissions", tags=["Permissions"])
    
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