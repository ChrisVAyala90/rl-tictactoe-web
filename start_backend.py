#!/usr/bin/env python3
"""
Startup script for the RL Tic-Tac-Toe backend server.
"""

import subprocess
import sys
import os

def main():
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    print("🚀 Starting RL Tic-Tac-Toe Backend Server...")
    print("📍 Backend directory:", os.getcwd())
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("=" * 50)
    
    try:
        # Start the FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        print("\n💡 Tips:")
        print("1. Make sure you're in the correct directory")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Train models first: python train_models.py")

if __name__ == "__main__":
    main()