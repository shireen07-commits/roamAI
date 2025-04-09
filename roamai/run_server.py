"""
Simple script to run the RoamAI API server.
"""

import logging
import uvicorn
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Run the FastAPI server."""
    logger.info("Starting RoamAI API server")
    
    # Set default host and port for Replit
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"Server will be available at http://{host}:{port}")
    logger.info(f"API documentation will be available at http://{host}:{port}/docs")
    
    # Run the FastAPI server with the app from roamai.api.app
    uvicorn.run(
        "roamai.api.app:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()