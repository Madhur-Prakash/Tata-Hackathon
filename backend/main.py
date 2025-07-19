import uvicorn
import sys
import os

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)