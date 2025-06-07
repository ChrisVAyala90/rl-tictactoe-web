from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import os

from api.simple_game_routes import router as game_router

# Create FastAPI app
app = FastAPI(
    title="RL Tic-Tac-Toe API",
    description="Backend API for Reinforcement Learning Tic-Tac-Toe game with difficulty levels",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include game routes
app.include_router(game_router)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    return """
    <html>
        <head>
            <title>RL Tic-Tac-Toe API</title>
        </head>
        <body>
            <h1>RL Tic-Tac-Toe API</h1>
            <p>Backend API for Reinforcement Learning Tic-Tac-Toe game</p>
            <h2>Available Endpoints:</h2>
            <ul>
                <li><a href="/docs">Interactive API Documentation</a></li>
                <li><a href="/redoc">ReDoc Documentation</a></li>
                <li><a href="/game/difficulties">Get Difficulty Levels</a></li>
            </ul>
            <h2>Features:</h2>
            <ul>
                <li>Multiple difficulty levels based on training epochs</li>
                <li>Both 3x3 and 4x4 game variants</li>
                <li>Special cells in 4x4 mode</li>
                <li>Real-time gameplay against AI agents</li>
            </ul>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "RL Tic-Tac-Toe API is running"}

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    print("Starting RL Tic-Tac-Toe API...")
    print("Simple rule-based AI ready - no training required!")

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )