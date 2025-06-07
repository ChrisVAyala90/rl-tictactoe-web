#!/bin/bash

echo "🚀 Starting RL Tic-Tac-Toe Backend (Simple)..."
echo "📁 Changing to backend directory..."

cd /Users/chrisvayala/RL/backend

echo "🌐 Server will be available at: http://localhost:8000"
echo "📖 API docs will be available at: http://localhost:8000/docs"
echo "🔧 Health check: http://localhost:8000/health"
echo "=" * 50

# Set PYTHONPATH and start server
export PYTHONPATH=/Users/chrisvayala/RL/backend:$PYTHONPATH
python3 -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload