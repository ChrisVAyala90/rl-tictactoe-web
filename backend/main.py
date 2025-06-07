"""
Minimal FastAPI backend for RL Tic-Tac-Toe
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from rl_game import RLGameEngine

app = FastAPI(title="RL Tic-Tac-Toe", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game storage
games = {}

class MoveRequest(BaseModel):
    game_id: str
    position: int

class TrainRequest(BaseModel):
    episodes: int = 10000

@app.get("/")
def root():
    return {"message": "RL Tic-Tac-Toe API", "status": "running"}

@app.post("/start")
def start_game():
    """Start a new game"""
    game_id = str(uuid.uuid4())
    engine = RLGameEngine()
    games[game_id] = engine
    
    return {
        "game_id": game_id,
        **engine.get_game_state()
    }

@app.post("/move")
def make_move(request: MoveRequest):
    """Make a move"""
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    engine = games[request.game_id]
    result = engine.make_move(request.position)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@app.post("/train")
def train_agent(request: TrainRequest):
    """Train the RL agent"""
    engine = RLGameEngine()
    result = engine.train_agent(request.episodes)
    return result

@app.post("/reset/{game_id}")
def reset_game(game_id: str):
    """Reset game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    engine = games[game_id]
    return engine.reset_game()

@app.post("/reset_ai")
def reset_ai():
    """Reset the AI - delete trained model"""
    import os
    model_path = "models/trained_agent.pkl"
    if os.path.exists(model_path):
        os.remove(model_path)
    
    # Clear all active games
    games.clear()
    
    return {
        "message": "AI reset successfully",
        "is_trained": False,
        "q_table_size": 0
    }

@app.get("/status")
def get_status():
    """Get agent training status"""
    engine = RLGameEngine()
    return {
        "is_trained": engine.is_trained,
        "q_table_size": len(engine.agent.q_table) if engine.is_trained else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)