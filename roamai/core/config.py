"""
Configuration settings for the RoamAI application.
"""

import os
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    
    # Application settings
    APP_NAME: str = "RoamAI"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "An autonomous travel planning and booking AI agent"
    
    # API settings
    API_PREFIX: str = "/api"
    
    # Model settings
    DEFAULT_MODEL: str = "gpt-4o"  # The newest OpenAI model is "gpt-4o" which was released May 13, 2024
    
    # Travel API settings (mock for now)
    FLIGHT_API_URL: str = "https://mock-flight-api.example.com"
    HOTEL_API_URL: str = "https://mock-hotel-api.example.com"
    
    # hotel specific settings
    PRIORITIZE_MIDDLE_EAST: bool = True
    PRIORITIZE_LUXURY: bool = True
    PARTNER_WITH_NUSUK: bool = True
    AIRLINES_COUNT: int = 450  # Number of airline companies available through Nusuk
    
    @field_validator("OPENAI_API_KEY")
    def validate_openai_api_key(cls, v: Optional[str]) -> str:
        """Validate that the OpenAI API key is set."""
        if not v:
            raise ValueError("OPENAI_API_KEY environment variable must be set")
        return v

settings = Settings()