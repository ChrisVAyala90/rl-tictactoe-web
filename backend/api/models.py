from pydantic import BaseModel
from typing import List, Optional

class GameStartRequest(BaseModel):
    difficulty: str
    game_size: int = 3  # 3 for classic, 4 for enhanced

class GameStartResponse(BaseModel):
    game_id: str
    board: List[str]
    size: int
    special_cells: List[int]
    available_moves: List[int]
    difficulty: str
    difficulty_info: dict

class MoveRequest(BaseModel):
    game_id: str
    position: int
    player: str = "O"  # Human is always O

class MoveResponse(BaseModel):
    success: bool
    board: List[str]
    ai_move: Optional[int] = None
    game_over: bool = False
    winner: Optional[str] = None
    message: str = ""
    available_moves: List[int] = []

class DifficultyInfo(BaseModel):
    episodes: int
    description: str
    trained: bool

class DifficultyListResponse(BaseModel):
    difficulties: dict[str, DifficultyInfo]
    
class GameStats(BaseModel):
    total_games: int
    wins: int
    losses: int
    draws: int
    win_rate: float
    current_streak: int
    best_streak: int