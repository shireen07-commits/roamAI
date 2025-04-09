"""
Server script to run the RoamAI FastAPI application.
"""

import os
import sys
import uvicorn

# Ensure PYTHONPATH includes the current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run the server."""
    # Load environment variables for production
    from roamai.api.app import app
    
    # Run the FastAPI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()