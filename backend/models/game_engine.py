import random
import pickle
import os
from typing import List, Tuple, Optional

class TicTacToe:
    def __init__(self, size: int = 3):
        self.size = size
        self.board = [' '] * (size * size)
        self.current_winner = None
        self.special_cells = []
        if size == 4:
            self.initialize_special_cells()

    def initialize_special_cells(self):
        """Initialize special cells for 4x4 game"""
        num_special_cells = random.randint(1, 4)
        self.special_cells = random.sample(range(16), num_special_cells)
        for cell in self.special_cells:
            self.board[cell] = 'X/O'

    def get_board_state(self) -> dict:
        """Return current board state as dict for API responses"""
        return {
            'board': self.board,
            'size': self.size,
            'current_winner': self.current_winner,
            'special_cells': self.special_cells,
            'available_moves': self.available_moves()
        }

    def available_moves(self) -> List[int]:
        """Returns list of available moves"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self) -> bool:
        """Check if there are empty squares"""
        return ' ' in self.board

    def make_move(self, square: int, letter: str) -> bool:
        """Make a move on the board"""
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_win(letter):
                self.current_winner = letter
            return True
        return False

    def check_win(self, letter: str) -> bool:
        """Check for win condition"""
        if self.size == 3:
            return self._check_win_3x3(letter)
        else:
            return self._check_win_4x4(letter)

    def _check_win_3x3(self, letter: str) -> bool:
        """Check win for 3x3 board"""
        # Check rows
        for i in range(3):
            if all(self.board[i*3 + j] == letter for j in range(3)):
                return True
        
        # Check columns
        for i in range(3):
            if all(self.board[i + j*3] == letter for j in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i*4] == letter for i in range(3)):
            return True
        if all(self.board[2 + i*2] == letter for i in range(3)):
            return True
        
        return False

    def _check_win_4x4(self, letter: str) -> bool:
        """Check win for 4x4 board including special cells"""
        win_conditions = []
        
        # Rows
        for i in range(4):
            win_conditions.append([self.board[i*4 + j] for j in range(4)])
        
        # Columns
        for i in range(4):
            win_conditions.append([self.board[i + j*4] for j in range(4)])
        
        # Diagonals
        win_conditions.append([self.board[i*5] for i in range(4)])
        win_conditions.append([self.board[(i+1)*3] for i in range(4)])
        
        for condition in win_conditions:
            count = sum(1 for cell in condition if cell == letter or cell == 'X/O')
            if count == 4:
                return True
        
        return False

class AITacAgent:
    def __init__(self, alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 1.0, epsilon_decay: float = 0.995, epsilon_min: float = 0.01):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.last_state = None
        self.last_action = None

    def get_state(self, board: List[str]) -> tuple:
        """Convert board to state tuple"""
        return tuple(board)

    def evaluate_position(self, board: List[str], board_size: int) -> float:
        """Evaluate position quality for better action selection"""
        score = 0.0
        
        # Center control bonus (for 3x3 board)
        if board_size == 3:
            if board[4] == 'X':
                score += 0.3
            elif board[4] == 'O':
                score -= 0.3
        
        # Corner control
        corners = [0, 2, 6, 8] if board_size == 3 else [0, 3, 12, 15]
        for corner in corners:
            if corner < len(board):
                if board[corner] == 'X':
                    score += 0.1
                elif board[corner] == 'O':
                    score -= 0.1
        
        return score
    
    def choose_action(self, state: tuple, available_actions: List[int], training: bool = False) -> int:
        """Choose action using epsilon-greedy policy with position evaluation"""
        # During gameplay (not training), use very low epsilon for exploitation
        epsilon = self.epsilon if training else max(self.epsilon_min, 0.02)
        
        if random.uniform(0, 1) < epsilon:
            action = random.choice(available_actions)
        else:
            # Enhanced action selection with position evaluation
            best_score = float('-inf')
            best_actions = []
            
            board_size = int(len(state) ** 0.5)
            
            for action in available_actions:
                # Get Q-value
                q_value = self.q_table.get((state, action), 0.0)
                
                # Add position evaluation bonus (only if not training to maintain learning)
                position_bonus = 0.0
                if not training:
                    temp_board = list(state)
                    temp_board[action] = 'X'
                    position_bonus = self.evaluate_position(temp_board, board_size) * 0.1
                
                total_score = q_value + position_bonus
                
                if total_score > best_score:
                    best_score = total_score
                    best_actions = [action]
                elif abs(total_score - best_score) < 1e-6:  # Handle floating point precision
                    best_actions.append(action)
            
            action = random.choice(best_actions) if best_actions else random.choice(available_actions)
        
        if training:
            self.last_state = state
            self.last_action = action
        
        return action
    
    def decay_epsilon(self):
        """Decay epsilon for less exploration over time"""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def get_q_value(self, state: tuple, action: int) -> float:
        """Get Q-value for state-action pair"""
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, reward: float, next_state: tuple, done: bool):
        """Update Q-value using Q-learning"""
        if self.last_state is None or self.last_action is None:
            return
            
        state = self.last_state
        action = self.last_action
        old_value = self.q_table.get((state, action), 0)
        
        if not done:
            next_available_actions = [i for i, spot in enumerate(next_state) if spot == ' ']
            future_q_values = [self.q_table.get((next_state, a), 0) for a in next_available_actions]
            future_reward = max(future_q_values) if future_q_values else 0
        else:
            future_reward = 0
        
        new_value = old_value + self.alpha * (reward + self.gamma * future_reward - old_value)
        self.q_table[(state, action)] = new_value

    def save_model(self, filepath: str):
        """Save Q-table to file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'q_table': self.q_table,
                'alpha': self.alpha,
                'gamma': self.gamma,
                'epsilon': self.epsilon,
                'epsilon_decay': self.epsilon_decay,
                'epsilon_min': self.epsilon_min
            }, f)

    @classmethod
    def load_model(cls, filepath: str):
        """Load Q-table from file"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        # Handle backward compatibility
        epsilon_decay = data.get('epsilon_decay', 0.995)
        epsilon_min = data.get('epsilon_min', 0.01)
        
        agent = cls(data['alpha'], data['gamma'], data['epsilon'], epsilon_decay, epsilon_min)
        agent.q_table = data['q_table']
        return agent