import random
import os
import math
from typing import Dict, List, Optional, Tuple
from .game_engine import TicTacToe, AITacAgent

# Difficulty levels with training episodes and descriptions
DIFFICULTY_LEVELS = {
    "beginner": {
        "episodes": 1000,
        "description": "Learning the basics - makes random moves",
        "model_file": "beginner_1k.pkl",
        "opponent_type": "random"
    },
    "easy": {
        "episodes": 10000,
        "description": "Understands basic patterns",
        "model_file": "easy_10k.pkl",
        "opponent_type": "random"
    },
    "medium": {
        "episodes": 50000,
        "description": "Strategic play with good tactics",
        "model_file": "medium_50k.pkl",
        "opponent_type": "mixed"
    },
    "hard": {
        "episodes": 200000,
        "description": "Advanced player with strong defense",
        "model_file": "hard_200k_minimax.pkl",
        "opponent_type": "minimax"
    },
    "expert": {
        "episodes": 50000,
        "description": "Master-level play trained vs perfect opponents",
        "model_file": "expert_proper_rl.pkl",
        "opponent_type": "perfect"
    }
}

class MinimaxAgent:
    """Minimax agent for providing stronger opposition"""
    
    def __init__(self, depth: int = 4):
        self.depth = depth
    
    def minimax(self, game: TicTacToe, depth: int, maximizing: bool, alpha: float = -math.inf, beta: float = math.inf) -> Tuple[int, Optional[int]]:
        """Minimax algorithm with alpha-beta pruning"""
        available_moves = game.available_moves()
        
        # Terminal cases
        if game.current_winner == 'O':  # Minimax player wins
            return 10 - depth, None
        elif game.current_winner == 'X':  # Opponent wins
            return depth - 10, None
        elif not available_moves or depth == 0:
            return 0, None  # Draw or depth limit
        
        best_move = None
        
        if maximizing:
            max_eval = -math.inf
            for move in available_moves:
                game.make_move(move, 'O')
                eval_score, _ = self.minimax(game, depth - 1, False, alpha, beta)
                game.board[move] = ' '  # Undo move
                game.current_winner = None
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in available_moves:
                game.make_move(move, 'X')
                eval_score, _ = self.minimax(game, depth - 1, True, alpha, beta)
                game.board[move] = ' '  # Undo move
                game.current_winner = None
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    def get_best_move(self, game: TicTacToe) -> int:
        """Get the best move using minimax"""
        _, best_move = self.minimax(game, self.depth, True)
        if best_move is None:
            return random.choice(game.available_moves())
        return best_move

class TrainingPipeline:
    def __init__(self, game_size: int = 3):
        self.game_size = game_size
        self.models_dir = os.path.join(os.path.dirname(__file__), 'model_checkpoints')
        os.makedirs(self.models_dir, exist_ok=True)
        self.minimax_agent = MinimaxAgent(depth=3 if game_size == 3 else 2)

    def get_strategic_reward(self, game: TicTacToe, action: int, player: str) -> float:
        """Calculate strategic reward based on position value"""
        # Center control bonus (for 3x3)
        if self.game_size == 3 and action == 4:
            return 0.5
        
        # Corner control bonus
        corners = [0, 2, 6, 8] if self.game_size == 3 else [0, 3, 12, 15]
        if action in corners:
            return 0.3
        
        # Blocking opponent win
        temp_game = TicTacToe(self.game_size)
        temp_game.board = game.board.copy()
        opponent = 'O' if player == 'X' else 'X'
        
        # Check if this move blocks an immediate win
        for move in temp_game.available_moves():
            temp_game.make_move(move, opponent)
            if temp_game.current_winner == opponent:
                temp_game.board[move] = ' '
                temp_game.current_winner = None
                if move == action:
                    return 2.0  # Good blocking move
            else:
                temp_game.board[move] = ' '
                temp_game.current_winner = None
        
        return 0.0
    
    def get_opponent_move(self, game: TicTacToe, opponent_type: str, trained_agent: Optional[AITacAgent] = None) -> int:
        """Get opponent move based on type"""
        available_moves = game.available_moves()
        
        if opponent_type == "random":
            return random.choice(available_moves)
        elif opponent_type == "minimax":
            return self.minimax_agent.get_best_move(game)
        elif opponent_type == "mixed":
            # 70% minimax, 30% random for varied training
            if random.random() < 0.7:
                return self.minimax_agent.get_best_move(game)
            else:
                return random.choice(available_moves)
        elif opponent_type == "self_play" and trained_agent:
            # Self-play: use another copy of the agent
            state = trained_agent.get_state(game.board)
            return trained_agent.choose_action(state, available_moves, training=False)
        else:
            return random.choice(available_moves)
    
    def train_agent(self, episodes: int, difficulty_name: str) -> AITacAgent:
        """Train an agent for specified number of episodes with advanced techniques"""
        config = DIFFICULTY_LEVELS[difficulty_name]
        opponent_type = config["opponent_type"]
        
        print(f"Training {difficulty_name} agent for {episodes} episodes with {opponent_type} opponents...")
        
        # Enhanced hyperparameters for different difficulties
        if episodes <= 1000:
            agent = AITacAgent(alpha=0.15, gamma=0.95, epsilon=1.0, epsilon_decay=0.99, epsilon_min=0.1)
        elif episodes <= 10000:
            agent = AITacAgent(alpha=0.12, gamma=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.05)
        elif episodes <= 50000:
            agent = AITacAgent(alpha=0.1, gamma=0.98, epsilon=1.0, epsilon_decay=0.9995, epsilon_min=0.02)
        else:
            agent = AITacAgent(alpha=0.08, gamma=0.99, epsilon=1.0, epsilon_decay=0.9998, epsilon_min=0.005)
        
        wins = 0
        losses = 0
        draws = 0
        
        # For self-play, create a copy of the agent for the opponent
        opponent_agent = None
        if opponent_type == "self_play":
            opponent_agent = AITacAgent(alpha=0.05, gamma=0.99, epsilon=0.1, epsilon_decay=0.999, epsilon_min=0.01)
        
        for episode in range(episodes):
            game = TicTacToe(self.game_size)
            state = agent.get_state(game.board)
            
            # Randomly choose who goes first for better learning
            agent_first = random.random() < 0.5
            
            if not agent_first:
                # Opponent goes first
                opponent_action = self.get_opponent_move(game, opponent_type, opponent_agent)
                game.make_move(opponent_action, 'O')
                state = agent.get_state(game.board)
            
            while True:
                # Agent's turn (X)
                available_moves = game.available_moves()
                if not available_moves:
                    draws += 1
                    break
                
                action = agent.choose_action(state, available_moves, training=True)
                
                # Add strategic reward
                strategic_reward = self.get_strategic_reward(game, action, 'X')
                
                game.make_move(action, 'X')
                next_state = agent.get_state(game.board)
                
                reward = strategic_reward
                done = False
                
                if game.current_winner == 'X':
                    reward += 15  # Higher reward for winning
                    wins += 1
                    done = True
                elif not game.empty_squares():
                    reward += 2  # Positive reward for draw
                    draws += 1
                    done = True
                else:
                    # Opponent's turn (O)
                    opponent_moves = game.available_moves()
                    if opponent_moves:
                        opponent_action = self.get_opponent_move(game, opponent_type, opponent_agent)
                        game.make_move(opponent_action, 'O')
                        
                        if game.current_winner == 'O':
                            reward -= 15  # Stronger negative reward for losing
                            losses += 1
                            done = True
                        elif not game.empty_squares():
                            reward += 2  # Positive reward for draw
                            draws += 1
                            done = True
                        else:
                            # Small negative reward for continuing
                            reward -= 0.05
                
                # Update Q-value
                agent.update_q_value(reward, next_state, done)
                state = next_state
                
                if done:
                    # Decay epsilon after each game
                    agent.decay_epsilon()
                    
                    # Update opponent agent in self-play
                    if opponent_type == "self_play" and opponent_agent and episode % 1000 == 0:
                        # Periodically copy main agent's knowledge to opponent
                        opponent_agent.q_table.update(agent.q_table)
                    break
            
            # Print progress every 10% of episodes
            if (episode + 1) % max(1, episodes // 10) == 0:
                win_rate = wins / (episode + 1) * 100
                print(f"Episode {episode + 1}/{episodes} - Win rate: {win_rate:.1f}%, Epsilon: {agent.epsilon:.3f}")
        
        # Final statistics
        total_games = wins + losses + draws
        print(f"Training completed!")
        print(f"Final stats - Wins: {wins} ({wins/total_games*100:.1f}%), "
              f"Losses: {losses} ({losses/total_games*100:.1f}%), "
              f"Draws: {draws} ({draws/total_games*100:.1f}%)")
        print(f"Final epsilon: {agent.epsilon:.3f}")
        print(f"Q-table size: {len(agent.q_table)} state-action pairs")
        
        return agent

    def train_all_difficulties(self, force_retrain: bool = False):
        """Train agents for all difficulty levels"""
        for difficulty, config in DIFFICULTY_LEVELS.items():
            model_path = os.path.join(self.models_dir, config["model_file"])
            
            # Skip if model exists and not forcing retrain
            if os.path.exists(model_path) and not force_retrain:
                print(f"Model for {difficulty} already exists. Skipping...")
                continue
            
            # Train the agent
            agent = self.train_agent(config["episodes"], difficulty)
            
            # Save the model
            agent.save_model(model_path)
            print(f"Saved {difficulty} model to {model_path}\n")

    def load_agent(self, difficulty: str) -> AITacAgent:
        """Load a trained agent for specified difficulty"""
        if difficulty not in DIFFICULTY_LEVELS:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        
        model_file = DIFFICULTY_LEVELS[difficulty]["model_file"]
        model_path = os.path.join(self.models_dir, model_file)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model for {difficulty} not found. Please train first.")
        
        return AITacAgent.load_model(model_path)

    def get_difficulty_info(self) -> Dict:
        """Get information about all difficulty levels"""
        info = {}
        for difficulty, config in DIFFICULTY_LEVELS.items():
            model_path = os.path.join(self.models_dir, config["model_file"])
            info[difficulty] = {
                "episodes": config["episodes"],
                "description": config["description"],
                "trained": os.path.exists(model_path)
            }
        return info

def main():
    """Train all models if run directly"""
    print("Starting training pipeline for 3x3 Tic-Tac-Toe...")
    pipeline = TrainingPipeline(game_size=3)
    pipeline.train_all_difficulties(force_retrain=False)
    
    print("\nStarting training pipeline for 4x4 Tic-Tac-Toe...")
    pipeline_4x4 = TrainingPipeline(game_size=4)
    pipeline_4x4.train_all_difficulties(force_retrain=False)
    
    print("All training completed!")

if __name__ == "__main__":
    main()