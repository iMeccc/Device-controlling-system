from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware # <-- 1. Import the CORS middleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# ... (rest of your imports remain the same) ...
from app.api.v1.endpoints import users as users_router
from app.api.v1.endpoints import instruments as instruments_router
from app.api.v1.endpoints import reservations as reservations_router

def create_tables():
    Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # --- 2. Add the CORS middleware ---
    # This is the "whitelist" of frontend domains that are allowed to talk to our API.
    origins = [
        "http://localhost:5173",  # The address of our Vue.js frontend
        # You can add other origins here, e.g., your production frontend URL
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    )
    
    # --- Include API Routers ---
    api_router = APIRouter()
    api_router.include_router(users_router.router, prefix="/users", tags=["Users"])
    api_router.include_router(instruments_router.router, prefix="/instruments", tags=["Instruments"])
    api_router.include_router(reservations_router.router, prefix="/reservations", tags=["Reservations"])
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

# ... (rest of your file remains the same) ...
create_tables()
app = create_app()

@app.get("/")
def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API"}