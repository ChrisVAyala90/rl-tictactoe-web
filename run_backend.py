#!/usr/bin/env python3
"""
Simple script to run the backend server.
"""
import uvicorn
import os
import sys

if __name__ == "__main__":
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Add backend directory to Python path
    sys.path.insert(0, os.getcwd())
    
    print("🚀 Starting RL Tic-Tac-Toe Backend...")
    print(f"📁 Working directory: {os.getcwd()}")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("🔧 Health check: http://localhost:8000/health")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
        reload_dirs=[os.getcwd()]
    )