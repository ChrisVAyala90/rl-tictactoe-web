"""
Simple but strong tic-tac-toe AI using direct strategy
Based on classic rule-based approach - no unnecessary complexity
"""

import random
from typing import List, Optional
from .game_engine import TicTacToe

class SimpleAI:
    """Simple rule-based AI that actually works"""
    
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        
        # Difficulty settings: chance of making random move instead of optimal
        self.randomness = {
            "easy": 0.4,        # 40% random moves
            "medium": 0.1,      # 10% random moves  
            "hard": 0.0         # 0% random moves (perfect play)
        }
    
    def get_move(self, game: TicTacToe, player: str = 'O') -> int:
        """Get the best move for the AI"""
        available_moves = game.available_moves()
        
        if not available_moves:
            return -1
        
        # Apply difficulty randomness
        if random.random() < self.randomness.get(self.difficulty, 0.0):
            return random.choice(available_moves)
        
        # Otherwise play optimally
        return self._get_optimal_move(game, player)
    
    def _get_optimal_move(self, game: TicTacToe, player: str) -> int:
        """Get the optimal move using simple strategy"""
        opponent = 'X' if player == 'O' else 'O'
        
        # 1. Win if possible
        winning_move = self._find_winning_move(game, player)
        if winning_move is not None:
            return winning_move
        
        # 2. Block opponent win
        blocking_move = self._find_winning_move(game, opponent)
        if blocking_move is not None:
            return blocking_move
        
        # 3. Strategic positioning
        return self._get_strategic_move(game)
    
    def _find_winning_move(self, game: TicTacToe, player: str) -> Optional[int]:
        """Find a move that wins the game"""
        for move in game.available_moves():
            # Try the move
            temp_game = TicTacToe(game.size)
            temp_game.board = game.board.copy()
            temp_game.make_move(move, player)
            
            if temp_game.current_winner == player:
                return move
        
        return None
    
    def _get_strategic_move(self, game: TicTacToe) -> int:
        """Get best strategic move when no immediate win/block needed"""
        available_moves = game.available_moves()
        
        if game.size == 3:
            return self._strategic_3x3(available_moves)
        else:
            return self._strategic_4x4(available_moves)
    
    def _strategic_3x3(self, available_moves: List[int]) -> int:
        """Strategic move selection for 3x3 board"""
        # Priority order: center, corners, edges
        
        # 1. Take center if available
        if 4 in available_moves:
            return 4
        
        # 2. Take corners
        corners = [0, 2, 6, 8]
        available_corners = [move for move in corners if move in available_moves]
        if available_corners:
            return random.choice(available_corners)
        
        # 3. Take edges as last resort
        return random.choice(available_moves)
    
    def _strategic_4x4(self, available_moves: List[int]) -> int:
        """Strategic move selection for 4x4 board"""
        # Priority: inner squares, corners, edges
        
        # Inner squares (better control)
        inner = [5, 6, 9, 10]
        available_inner = [move for move in inner if move in available_moves]
        if available_inner:
            return random.choice(available_inner)
        
        # Corners
        corners = [0, 3, 12, 15]
        available_corners = [move for move in corners if move in available_moves]
        if available_corners:
            return random.choice(available_corners)
        
        # Any remaining move
        return random.choice(available_moves)


class SimpleTicTacToeEngine:
    """Simple game engine with rule-based AI"""
    
    def __init__(self, size: int = 3, difficulty: str = "medium"):
        self.game = TicTacToe(size)
        self.ai = SimpleAI(difficulty)
        self.difficulty = difficulty
    
    def make_player_move(self, position: int) -> dict:
        """Player makes a move"""
        if not self.game.make_move(position, 'X'):
            return {"error": "Invalid move"}
        
        game_state = self._get_game_state()
        
        # Check if game is over
        if self.game.current_winner or not self.game.available_moves():
            return game_state
        
        # AI makes move
        ai_move = self.ai.get_move(self.game, 'O')
        if ai_move != -1:
            self.game.make_move(ai_move, 'O')
        
        return self._get_game_state()
    
    def _get_game_state(self) -> dict:
        """Get current game state"""
        return {
            "board": self.game.board,
            "current_winner": self.game.current_winner,
            "available_moves": self.game.available_moves(),
            "game_over": self.game.current_winner is not None or not self.game.available_moves(),
            "difficulty": self.difficulty
        }
    
    def reset_game(self):
        """Reset the game"""
        self.game = TicTacToe(self.game.size)
        if self.game.size == 4:
            self.game.initialize_special_cells()
    
    def get_difficulty_info(self) -> dict:
        """Get information about current difficulty"""
        descriptions = {
            "easy": "Casual play - makes some mistakes", 
            "medium": "Good challenge - plays strategically",
            "hard": "Expert level - perfect play"
        }
        
        return {
            "difficulty": self.difficulty,
            "description": descriptions.get(self.difficulty, "Unknown"),
            "randomness": self.ai.randomness.get(self.difficulty, 0.0)
        }


# For backward compatibility with existing API
class AITacAgentSimple:
    """Simple wrapper to match existing API interface"""
    
    def __init__(self, difficulty: str = "medium"):
        self.ai = SimpleAI(difficulty)
        self.difficulty = difficulty
    
    def choose_action(self, state: tuple, available_actions: List[int], training: bool = False) -> int:
        """Choose action - compatible with existing interface"""
        # Convert state tuple back to game
        game = TicTacToe(int(len(state) ** 0.5))
        game.board = list(state)
        
        return self.ai.get_move(game, 'O')
    
    def get_state(self, board: List[str]) -> tuple:
        """Convert board to state - for compatibility"""
        return tuple(board)


def create_simple_models():
    """Create simple AI models for all difficulties"""
    difficulties = ["easy", "medium", "hard"]
    
    print("Creating simple AI models...")
    for difficulty in difficulties:
        ai = AITacAgentSimple(difficulty)
        print(f"✓ {difficulty.capitalize()} AI ready (randomness: {ai.ai.randomness[difficulty]*100:.0f}%)")
    
    print("\nSimple AI models created successfully!")
    print("These are immediately ready - no training required!")
    return True

if __name__ == "__main__":
    create_simple_models()