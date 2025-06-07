from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.game_engine import TicTacToe, AITacAgent
from models.training_pipeline import TrainingPipeline, DIFFICULTY_LEVELS
from .models import (
    GameStartRequest, GameStartResponse, MoveRequest, MoveResponse,
    DifficultyListResponse, DifficultyInfo, GameStats
)

router = APIRouter(prefix="/game", tags=["game"])

# In-memory game storage (in production, use Redis or database)
active_games: Dict[str, dict] = {}
game_stats: Dict[str, GameStats] = {}

@router.get("/difficulties", response_model=DifficultyListResponse)
async def get_difficulties():
    """Get all available difficulty levels and their training status"""
    pipeline_3x3 = TrainingPipeline(game_size=3)
    pipeline_4x4 = TrainingPipeline(game_size=4)
    
    difficulties_3x3 = pipeline_3x3.get_difficulty_info()
    difficulties_4x4 = pipeline_4x4.get_difficulty_info()
    
    # Combine both game sizes
    all_difficulties = {}
    for diff, info in difficulties_3x3.items():
        all_difficulties[f"{diff}_3x3"] = DifficultyInfo(**info)
    for diff, info in difficulties_4x4.items():
        all_difficulties[f"{diff}_4x4"] = DifficultyInfo(**info)
    
    return DifficultyListResponse(difficulties=all_difficulties)

@router.post("/start", response_model=GameStartResponse)
async def start_game(request: GameStartRequest):
    """Start a new game with specified difficulty and size"""
    try:
        # Parse difficulty (remove size suffix if present)
        base_difficulty = request.difficulty.replace("_3x3", "").replace("_4x4", "")
        
        if base_difficulty not in DIFFICULTY_LEVELS:
            raise HTTPException(status_code=400, detail=f"Invalid difficulty: {base_difficulty}")
        
        # Create game
        game = TicTacToe(size=request.game_size)
        
        # Load trained agent
        pipeline = TrainingPipeline(game_size=request.game_size)
        try:
            agent = pipeline.load_agent(base_difficulty)
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, 
                detail=f"Model for {base_difficulty} not trained yet. Please train models first."
            )
        
        # Generate game ID and store game state
        game_id = str(uuid.uuid4())
        active_games[game_id] = {
            "game": game,
            "agent": agent,
            "difficulty": base_difficulty,
            "moves_count": 0
        }
        
        # Get difficulty info
        difficulty_info = DIFFICULTY_LEVELS[base_difficulty]
        
        return GameStartResponse(
            game_id=game_id,
            board=game.board,
            size=game.size,
            special_cells=game.special_cells,
            available_moves=game.available_moves(),
            difficulty=base_difficulty,
            difficulty_info=difficulty_info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/move", response_model=MoveResponse)
async def make_move(request: MoveRequest):
    """Make a human move and get AI response"""
    if request.game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_state = active_games[request.game_id]
    game = game_state["game"]
    agent = game_state["agent"]
    
    try:
        # Validate human move
        if request.position not in game.available_moves():
            return MoveResponse(
                success=False,
                board=game.board,
                message="Invalid move. Position already taken or out of bounds."
            )
        
        # Make human move
        game.make_move(request.position, "O")
        game_state["moves_count"] += 1
        
        # Check if human won
        if game.current_winner == "O":
            return MoveResponse(
                success=True,
                board=game.board,
                game_over=True,
                winner="O",
                message="Congratulations! You won!",
                available_moves=[]
            )
        
        # Check for draw
        if not game.empty_squares():
            return MoveResponse(
                success=True,
                board=game.board,
                game_over=True,
                winner=None,
                message="It's a draw!",
                available_moves=[]
            )
        
        # AI's turn
        state = agent.get_state(game.board)
        available_moves = game.available_moves()
        
        if not available_moves:
            # This shouldn't happen, but handle it gracefully
            return MoveResponse(
                success=True,
                board=game.board,
                game_over=True,
                winner=None,
                message="It's a draw!",
                available_moves=[]
            )
        
        # AI makes move (training=False ensures no learning during gameplay)
        ai_move = agent.choose_action(state, available_moves, training=False)
        game.make_move(ai_move, "X")
        game_state["moves_count"] += 1
        
        # Check if AI won
        if game.current_winner == "X":
            return MoveResponse(
                success=True,
                board=game.board,
                ai_move=ai_move,
                game_over=True,
                winner="X",
                message="AI wins! Better luck next time.",
                available_moves=[]
            )
        
        # Check for draw after AI move
        if not game.empty_squares():
            return MoveResponse(
                success=True,
                board=game.board,
                ai_move=ai_move,
                game_over=True,
                winner=None,
                message="It's a draw!",
                available_moves=[]
            )
        
        # Game continues
        return MoveResponse(
            success=True,
            board=game.board,
            ai_move=ai_move,
            available_moves=game.available_moves(),
            message="Your turn!"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/end/{game_id}")
async def end_game(game_id: str):
    """End a game and clean up resources"""
    if game_id in active_games:
        del active_games[game_id]
        return {"message": "Game ended successfully"}
    else:
        raise HTTPException(status_code=404, detail="Game not found")

@router.get("/stats")
async def get_game_stats():
    """Get global game statistics"""
    return {
        "active_games": len(active_games),
        "total_games_played": len(game_stats)
    }