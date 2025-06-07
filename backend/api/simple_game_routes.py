from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.simple_ai import SimpleTicTacToeEngine
from .models import (
    GameStartRequest, GameStartResponse, MoveRequest, MoveResponse,
    DifficultyListResponse, DifficultyInfo, GameStats
)

router = APIRouter(prefix="/game", tags=["game"])

# In-memory game storage
active_games: Dict[str, SimpleTicTacToeEngine] = {}
game_stats: Dict[str, GameStats] = {}

@router.get("/difficulties", response_model=DifficultyListResponse)
async def get_difficulties():
    """Get all available difficulty levels"""
    
    difficulties = {
        "easy": {
            "episodes": 0,
            "description": "Casual play - makes some mistakes",
            "trained": True
        },
        "medium": {
            "episodes": 0,
            "description": "Good challenge - plays strategically",
            "trained": True
        },
        "hard": {
            "episodes": 0,
            "description": "Expert level - perfect play",
            "trained": True
        }
    }
    
    # Convert to required format (dictionary of DifficultyInfo objects)
    difficulty_dict = {}
    for name, info in difficulties.items():
        difficulty_dict[name] = DifficultyInfo(
            description=info["description"],
            episodes=info["episodes"],
            trained=info["trained"]
        )
    
    return DifficultyListResponse(difficulties=difficulty_dict)

@router.post("/start", response_model=GameStartResponse)
async def start_game(request: GameStartRequest):
    """Start a new game with specified difficulty and size"""
    try:
        # Set default difficulty if not provided or validate if provided
        difficulty = getattr(request, 'difficulty', 'medium') or 'medium'
        valid_difficulties = ["easy", "medium", "hard"]
        if difficulty not in valid_difficulties:
            raise HTTPException(status_code=400, detail=f"Invalid difficulty: {difficulty}")
        
        # Validate game size
        if request.game_size not in [3, 4]:
            raise HTTPException(status_code=400, detail=f"Invalid game size: {request.game_size}")
        
        # Create simple AI engine
        game_engine = SimpleTicTacToeEngine(
            size=request.game_size,
            difficulty=difficulty
        )
        
        # Generate game ID
        game_id = str(uuid.uuid4())
        active_games[game_id] = game_engine
        
        # Initialize stats  
        game_stats[game_id] = GameStats(
            total_games=0,
            wins=0,
            losses=0,
            draws=0,
            win_rate=0.0,
            current_streak=0,
            best_streak=0
        )
        
        return GameStartResponse(
            game_id=game_id,
            board=game_engine.game.board,
            size=request.game_size,
            difficulty=difficulty,
            special_cells=game_engine.game.special_cells if request.game_size == 4 else [],
            available_moves=game_engine.game.available_moves(),
            difficulty_info={"description": f"{difficulty} difficulty"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start game: {str(e)}")

@router.post("/move", response_model=MoveResponse)
async def make_move(request: MoveRequest):
    """Make a move in an existing game"""
    if request.game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        game_engine = active_games[request.game_id]
        
        # Make player move and get AI response
        result = game_engine.make_player_move(request.position)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Update stats if game is over
        if result["game_over"]:
            stats = game_stats[request.game_id]
            stats.total_games += 1
            
            if result["current_winner"] == 'X':
                stats.wins += 1
            elif result["current_winner"] == 'O':
                stats.losses += 1
            else:
                stats.draws += 1
            
            # Update win rate
            stats.win_rate = stats.wins / stats.total_games if stats.total_games > 0 else 0.0
        
        return MoveResponse(
            success=True,
            board=result["board"],
            ai_move=None,  # Could track this if needed
            game_over=result["game_over"],
            winner=result["current_winner"],
            message="Move successful",
            available_moves=result["available_moves"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to make move: {str(e)}")

@router.delete("/end/{game_id}")
async def end_game(game_id: str):
    """End and cleanup a game"""
    if game_id in active_games:
        del active_games[game_id]
    if game_id in game_stats:
        del game_stats[game_id]
    return {"message": "Game ended successfully"}

@router.post("/reset/{game_id}")
async def reset_game(game_id: str):
    """Reset an existing game"""
    if game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        game_engine = active_games[game_id]
        game_engine.reset_game()
        
        return {
            "board": game_engine.game.board,
            "available_moves": game_engine.game.available_moves(),
            "special_cells": game_engine.game.special_cells if game_engine.game.size == 4 else []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset game: {str(e)}")

@router.get("/stats/{game_id}", response_model=GameStats)
async def get_game_stats(game_id: str):
    """Get statistics for a game session"""
    if game_id not in game_stats:
        raise HTTPException(status_code=404, detail="Game stats not found")
    
    return game_stats[game_id]

@router.get("/info/{game_id}")
async def get_game_info(game_id: str):
    """Get current game information"""
    if game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_engine = active_games[game_id]
    difficulty_info = game_engine.get_difficulty_info()
    
    return {
        "game_id": game_id,
        "board": game_engine.game.board,
        "current_winner": game_engine.game.current_winner,
        "available_moves": game_engine.game.available_moves(),
        "game_size": game_engine.game.size,
        "difficulty_info": difficulty_info,
        "special_cells": game_engine.game.special_cells if game_engine.game.size == 4 else []
    }