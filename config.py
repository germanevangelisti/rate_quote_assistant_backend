from pydantic_settings import BaseSettings
import os
from enum import Enum

class Environment(str, Enum):
    LOCAL = "local"
    TESTING = "testing"
    PRODUCTION = "production"

class Settings(BaseSettings):
    """Application settings."""
    
    ENV: Environment = Environment.LOCAL
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    
    # WebSocket URLs
    WS_URL_LOCAL: str = "ws://127.0.0.1:8000/ws/quote"
    WS_URL_TESTING: str = "wss://rate-quote-assistant-backend.onrender.com/ws/quote"
    
    @property
    def ws_url(self) -> str:
        """Return the appropriate WebSocket URL based on environment."""
        if self.ENV == Environment.LOCAL:
            return self.WS_URL_LOCAL
        elif self.ENV == Environment.TESTING:
            return self.WS_URL_TESTING
        return self.WS_URL_LOCAL  # Default to local
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instantiate the settings object
settings = Settings()

def get_settings():
    return settings 