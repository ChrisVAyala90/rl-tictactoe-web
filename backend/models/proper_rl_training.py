import random
import math
import os
import pickle
from typing import Dict, List, Optional, Tuple
from .game_engine import TicTacToe, AITacAgent

class PerfectTicTacToeTeacher:
    """A perfect tic-tac-toe player that never loses - used to train RL agents"""
    
    def __init__(self, depth: int = 9):
        self.depth = depth
        
    def evaluate_position(self, game: TicTacToe, player: str) -> int:
        """Evaluate terminal positions"""
        if game.current_winner == player:
            return 10
        elif game.current_winner and game.current_winner != player:
            return -10
        else:
            return 0
    
    def minimax(self, game: TicTacToe, depth: int, is_maximizing: bool, 
                player: str, opponent: str, alpha: float = -math.inf, beta: float = math.inf) -> int:
        """Minimax with alpha-beta pruning"""
        # Terminal case
        if game.current_winner or not game.available_moves() or depth == 0:
            return self.evaluate_position(game, player)
        
        if is_maximizing:
            max_eval = -math.inf
            for move in game.available_moves():
                # Make move
                game.make_move(move, player)
                eval_score = self.minimax(game, depth - 1, False, player, opponent, alpha, beta)
                # Undo move
                game.board[move] = ' '
                game.current_winner = None
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in game.available_moves():
                # Make move
                game.make_move(move, opponent)
                eval_score = self.minimax(game, depth - 1, True, player, opponent, alpha, beta)
                # Undo move
                game.board[move] = ' '
                game.current_winner = None
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_best_move(self, game: TicTacToe, player: str = 'O') -> int:
        """Get the optimal move"""
        best_move = None
        best_value = -math.inf
        opponent = 'X' if player == 'O' else 'O'
        
        for move in game.available_moves():
            # Make move
            game.make_move(move, player)
            move_value = self.minimax(game, self.depth - 1, False, player, opponent)
            # Undo move
            game.board[move] = ' '
            game.current_winner = None
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
        
        return best_move if best_move is not None else random.choice(game.available_moves())

class CurriculumTraining:
    """Implements curriculum learning for RL agents"""
    
    def __init__(self, game_size: int = 3):
        self.game_size = game_size
        self.perfect_teacher = PerfectTicTacToeTeacher()
        
    def get_opponent_move(self, game: TicTacToe, curriculum_level: float, trained_snapshots: List = None) -> int:
        """
        Get opponent move based on curriculum level (0.0 = random, 1.0 = perfect)
        curriculum_level gradually increases during training
        """
        available_moves = game.available_moves()
        
        # Curriculum stages:
        if curriculum_level < 0.2:
            # Stage 1: Pure random (learning basics)
            return random.choice(available_moves)
        elif curriculum_level < 0.4:
            # Stage 2: 70% random, 30% perfect (learning to not lose immediately)
            if random.random() < 0.3:
                return self.perfect_teacher.get_best_move(game, 'O')
            else:
                return random.choice(available_moves)
        elif curriculum_level < 0.6:
            # Stage 3: 50% random, 50% perfect (learning tactics)
            if random.random() < 0.5:
                return self.perfect_teacher.get_best_move(game, 'O')
            else:
                return random.choice(available_moves)
        elif curriculum_level < 0.8:
            # Stage 4: 20% random, 80% perfect (advanced play)
            if random.random() < 0.8:
                return self.perfect_teacher.get_best_move(game, 'O')
            else:
                return random.choice(available_moves)
        else:
            # Stage 5: 95% perfect, 5% random (near-perfect opponents)
            if random.random() < 0.95:
                return self.perfect_teacher.get_best_move(game, 'O')
            else:
                return random.choice(available_moves)

class ProperRLAgent(AITacAgent):
    """Enhanced RL agent with proper training techniques"""
    
    def __init__(self, alpha: float = 0.1, gamma: float = 0.95, 
                 epsilon_start: float = 0.9, epsilon_end: float = 0.01, 
                 epsilon_decay_episodes: int = 100000):
        super().__init__(alpha, gamma, epsilon_start, 0.999, epsilon_end)
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay_episodes = epsilon_decay_episodes
        self.episode_count = 0
        self.initialize_value_function()
        
    def update_epsilon(self):
        """Linear epsilon decay over specified episodes"""
        if self.episode_count < self.epsilon_decay_episodes:
            decay_ratio = self.episode_count / self.epsilon_decay_episodes
            self.epsilon = self.epsilon_start * (1 - decay_ratio) + self.epsilon_end * decay_ratio
        else:
            self.epsilon = self.epsilon_end
        self.episode_count += 1
    
    def initialize_value_function(self):
        """Bootstrap with domain knowledge for faster convergence"""
        # Initialize center and corner positions with positive values
        empty_board = tuple([' '] * 9)
        
        # Center is valuable
        self.q_table[(empty_board, 4)] = 0.5
        
        # Corners are valuable  
        for corner in [0, 2, 6, 8]:
            self.q_table[(empty_board, corner)] = 0.3
            
        # Edges are less valuable
        for edge in [1, 3, 5, 7]:
            self.q_table[(empty_board, edge)] = 0.1
    
    def get_state_value(self, state: tuple) -> float:
        """Get the maximum Q-value for a state (state value function)"""
        available_actions = [i for i, spot in enumerate(state) if spot == ' ']
        if not available_actions:
            return 0.0
        return max(self.q_table.get((state, action), 0.0) for action in available_actions)
    
    def choose_action(self, state: tuple, available_actions: List[int], training: bool = False) -> int:
        """Enhanced action selection with immediate win/block detection"""
        if not training:
            # During gameplay, check for immediate wins/blocks first
            temp_game = TicTacToe(3)
            temp_game.board = list(state)
            
            # Check for winning moves first
            for action in available_actions:
                temp_game.board[action] = 'X'
                if temp_game.check_win('X'):
                    temp_game.board[action] = ' '
                    return action
                temp_game.board[action] = ' '
            
            # Check for blocking moves
            for action in available_actions:
                temp_game.board[action] = 'O'
                if temp_game.check_win('O'):
                    temp_game.board[action] = ' '
                    return action
                temp_game.board[action] = ' '
        
        # Use parent's epsilon-greedy selection
        return super().choose_action(state, available_actions, training)

class ProperRLTraining:
    """Proper RL training pipeline with curriculum learning"""
    
    def __init__(self, game_size: int = 3):
        self.game_size = game_size
        self.curriculum = CurriculumTraining(game_size)
        self.models_dir = os.path.join(os.path.dirname(__file__), 'model_checkpoints')
        os.makedirs(self.models_dir, exist_ok=True)
    
    def train_proper_rl_agent(self, episodes: int, difficulty_name: str, 
                             target_win_rate: float = 0.1) -> ProperRLAgent:
        """
        Train RL agent with proper curriculum and convergence criteria
        target_win_rate: Against perfect opponent (0.0 = never lose, only draw/win)
        """
        print(f"Training {difficulty_name} with proper RL for {episodes} episodes...")
        print(f"Target: Win rate ≥ {target_win_rate*100:.1f}% vs perfect opponent")
        
        # Hyperparameters based on difficulty
        if difficulty_name == "beginner":
            agent = ProperRLAgent(alpha=0.3, gamma=0.9, epsilon_start=0.9, 
                                epsilon_end=0.4, epsilon_decay_episodes=episodes//3)
        elif difficulty_name == "easy":
            agent = ProperRLAgent(alpha=0.2, gamma=0.95, epsilon_start=0.7, 
                                epsilon_end=0.2, epsilon_decay_episodes=episodes//3)
        elif difficulty_name == "medium":
            agent = ProperRLAgent(alpha=0.15, gamma=0.98, epsilon_start=0.5, 
                                epsilon_end=0.1, epsilon_decay_episodes=episodes//2)
        elif difficulty_name == "hard":
            agent = ProperRLAgent(alpha=0.1, gamma=0.99, epsilon_start=0.3, 
                                epsilon_end=0.05, epsilon_decay_episodes=episodes//2)
        else:  # expert
            agent = ProperRLAgent(alpha=0.05, gamma=0.995, epsilon_start=0.2, 
                                epsilon_end=0.01, epsilon_decay_episodes=episodes//2)
        
        wins = losses = draws = 0
        recent_performance = []
        best_performance = 0
        
        for episode in range(episodes):
            game = TicTacToe(self.game_size)
            state = agent.get_state(game.board)
            
            # Curriculum level increases over training
            curriculum_level = min(episode / (episodes * 0.8), 1.0)
            
            # Agent goes first (X)
            while game.available_moves():
                # Agent's turn
                available_moves = game.available_moves()
                action = agent.choose_action(state, available_moves, training=True)
                game.make_move(action, 'X')
                
                if game.current_winner == 'X':
                    reward = 10
                    wins += 1
                    agent.update_q_value(reward, agent.get_state(game.board), True)
                    break
                elif not game.available_moves():
                    reward = 5  # Draw is good against perfect opponent
                    draws += 1
                    agent.update_q_value(reward, agent.get_state(game.board), True)
                    break
                
                # Opponent's turn (curriculum-based)
                opponent_action = self.curriculum.get_opponent_move(game, curriculum_level)
                game.make_move(opponent_action, 'O')
                next_state = agent.get_state(game.board)
                
                if game.current_winner == 'O':
                    reward = -10
                    losses += 1
                    agent.update_q_value(reward, next_state, True)
                    break
                elif not game.available_moves():
                    reward = 5  # Draw is good
                    draws += 1
                    agent.update_q_value(reward, next_state, True)
                    break
                else:
                    # Continue game
                    reward = 0
                    agent.update_q_value(reward, next_state, False)
                    state = next_state
            
            # Update epsilon
            agent.update_epsilon()
            
            # Track performance
            if episode > 0 and episode % 10000 == 0:
                total_games = wins + losses + draws
                win_rate = wins / total_games if total_games > 0 else 0
                draw_rate = draws / total_games if total_games > 0 else 0
                no_loss_rate = (wins + draws) / total_games if total_games > 0 else 0
                
                recent_performance.append(no_loss_rate)
                if len(recent_performance) > 10:
                    recent_performance.pop(0)
                
                avg_recent = sum(recent_performance) / len(recent_performance)
                
                print(f"Episode {episode:,}/{episodes:,} - Win: {win_rate:.1%}, "
                      f"Draw: {draw_rate:.1%}, No-Loss: {no_loss_rate:.1%}, "
                      f"Avg Recent: {avg_recent:.1%}, ε: {agent.epsilon:.3f}, "
                      f"Curriculum: {curriculum_level:.1%}")
                
                if avg_recent > best_performance:
                    best_performance = avg_recent
        
        # Final statistics
        total_games = wins + losses + draws
        final_win_rate = wins / total_games if total_games > 0 else 0
        final_draw_rate = draws / total_games if total_games > 0 else 0
        final_no_loss_rate = (wins + draws) / total_games if total_games > 0 else 0
        
        print(f"\n{difficulty_name.upper()} TRAINING COMPLETED:")
        print(f"Final Performance: Win: {final_win_rate:.1%}, Draw: {final_draw_rate:.1%}, "
              f"No-Loss: {final_no_loss_rate:.1%}")
        print(f"Q-table size: {len(agent.q_table):,} state-action pairs")
        print(f"Best performance: {best_performance:.1%}")
        
        return agent
    
    def train_all_proper_difficulties(self):
        """Train all difficulties with proper RL"""
        difficulties = {
            "beginner": {"episodes": 50000, "target": 0.0},    # Just learn not to lose immediately
            "easy": {"episodes": 100000, "target": 0.05},      # Occasional draws vs perfect
            "medium": {"episodes": 200000, "target": 0.15},    # Regular draws vs perfect  
            "hard": {"episodes": 500000, "target": 0.25},      # Often draws vs perfect
            "expert": {"episodes": 1000000, "target": 0.35}    # Usually draws vs perfect
        }
        
        for difficulty, config in difficulties.items():
            agent = self.train_proper_rl_agent(
                config["episodes"], 
                difficulty,
                config["target"]
            )
            
            # Save model
            model_path = os.path.join(self.models_dir, f"{difficulty}_proper_rl.pkl")
            agent.save_model(model_path)
            print(f"Saved {difficulty} model to {model_path}\n")

def main():
    """Train proper RL models"""
    print("Starting PROPER RL training pipeline...")
    trainer = ProperRLTraining(game_size=3)
    trainer.train_all_proper_difficulties()
    print("Proper RL training completed!")

if __name__ == "__main__":
    main()