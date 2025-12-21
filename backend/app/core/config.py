from pydantic_settings import BaseSettings
from typing import Optional, TYPE_CHECKING

class Settings(BaseSettings):
    # --- Project Settings ---
    PROJECT_NAME: str = "Device Controlling System"
    API_V1_STR: str = "/api/v1"
    
    # --- Database Settings (will be loaded from .env file) ---
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # --- Security Settings (will be loaded from .env file) ---
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    def model_post_init(self, __context):
        """
        Construct the full database URI after the model is initialized.
        """
        if self.SQLALCHEMY_DATABASE_URI is None:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )

    class Config:
        # This tells pydantic-settings where to load variables from at RUNTIME
        env_file = ".env"
        env_file_encoding = "utf-8"

# This block resolves the static analysis error from Pylance.
if TYPE_CHECKING:
    settings: Settings
else:
    settings = Settings()