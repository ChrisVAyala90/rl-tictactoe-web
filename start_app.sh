#!/bin/bash

echo "🎮 Starting RL Tic-Tac-Toe Application..."
echo "=================================="

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f uvicorn 2>/dev/null || true
pkill -f vite 2>/dev/null || true
sleep 2

# Start backend in background
echo "🚀 Starting backend server..."
cd /Users/chrisvayala/RL/backend
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    echo "   Attempt $i/10..."
    sleep 2
done

# Start frontend in background
echo "🎨 Starting frontend server..."
cd /Users/chrisvayala/RL/frontend
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
for i in {1..15}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend is ready!"
        break
    fi
    echo "   Attempt $i/15..."
    sleep 2
done

echo ""
echo "🎉 Application is ready!"
echo "=================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Process IDs:"
echo "   Backend:  $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo ""
echo "💡 To stop the servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📜 Logs:"
echo "   Backend:  tail -f /Users/chrisvayala/RL/backend/backend.log"
echo "   Frontend: tail -f /Users/chrisvayala/RL/frontend/frontend.log"
echo ""

# Keep the script running and show status
while true; do
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend process died!"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ Frontend process died!"
        break
    fi
    sleep 5
done