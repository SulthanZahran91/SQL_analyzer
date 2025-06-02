#!/usr/bin/env python3
"""
Startup script for SQL Query Analyzer FastAPI backend
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Start the FastAPI server"""
    
    # Add the current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    print("🚀 Starting SQL Query Analyzer Backend...")
    print("📍 API Documentation: http://localhost:8000/docs")
    print("📍 Health Check: http://localhost:8000/health")
    print("📍 Frontend should connect to: http://localhost:8000")
    print("\n" + "="*50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down SQL Query Analyzer Backend...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()