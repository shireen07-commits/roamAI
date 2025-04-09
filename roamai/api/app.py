"""
Main FastAPI application for RoamAI API.
"""

import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ..core.config import settings
from .travel import router as travel_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(travel_router, prefix=settings.API_PREFIX)

@app.get("/", tags=["Health"])
async def health_check():
    """Check if the API is running."""
    return {"status": "ok", "message": f"{settings.APP_NAME} API is running"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for the API."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )