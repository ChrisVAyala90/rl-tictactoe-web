"""
Simplified RL Tic-Tac-Toe - Just your assignment5 Q-learning agent
"""
import random
import pickle
import os

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in column]):
            return True
        
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def reset(self):
        self.board = [' '] * 9
        self.current_winner = None

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state(self, board):
        return tuple(board)

    def choose_action(self, state, available_actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(available_actions)
        else:
            q_values = [self.q_table.get((state, action), 0) for action in available_actions]
            max_q = max(q_values)
            best_actions = [action for action, q_val in zip(available_actions, q_values) if q_val == max_q]
            return random.choice(best_actions)

    def update_q_value(self, state, action, reward, next_state, done):
        old_value = self.q_table.get((state, action), 0)
        future_reward = 0
        
        if not done:
            next_available_actions = [i for i in range(9) if next_state[i] == ' ']
            if next_available_actions:
                future_q_values = [self.q_table.get((next_state, a), 0) for a in next_available_actions]
                future_reward = max(future_q_values)
        
        new_value = old_value + self.alpha * (reward + self.gamma * future_reward - old_value)
        self.q_table[(state, action)] = new_value

    def save_model(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'q_table': self.q_table,
                'alpha': self.alpha,
                'gamma': self.gamma,
                'epsilon': self.epsilon
            }, f)

    @classmethod
    def load_model(cls, filepath):
        if not os.path.exists(filepath):
            return cls()
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        agent = cls(data['alpha'], data['gamma'], data['epsilon'])
        agent.q_table = data['q_table']
        return agent

def train_agent(episodes=10000):
    """Train the Q-learning agent"""
    agent = QLearningAgent()
    
    for episode in range(episodes):
        game = TicTacToe()
        state = agent.get_state(game.board)
        
        while True:
            # Agent's turn (X)
            available_moves = game.available_moves()
            if not available_moves:
                break
                
            action = agent.choose_action(state, available_moves)
            game.make_move(action, 'X')
            
            next_state = agent.get_state(game.board)
            reward = 0
            done = False
            
            if game.current_winner == 'X':
                reward = 1
                done = True
            elif not game.available_moves():
                done = True
            
            if not done:
                # Opponent move (O) - mix of random and strategic
                opponent_moves = game.available_moves()
                if opponent_moves:
                    # 20% of the time, use strategic opponent to explore more states
                    if random.random() < 0.2:
                        # Simple strategic opponent: try to win, then block, then random
                        strategic_move = None
                        
                        # Try to win
                        for move in opponent_moves:
                            temp_game = TicTacToe()
                            temp_game.board = game.board.copy()
                            temp_game.make_move(move, 'O')
                            if temp_game.current_winner == 'O':
                                strategic_move = move
                                break
                        
                        # Try to block
                        if strategic_move is None:
                            for move in opponent_moves:
                                temp_game = TicTacToe()
                                temp_game.board = game.board.copy()
                                temp_game.make_move(move, 'X')
                                if temp_game.current_winner == 'X':
                                    strategic_move = move
                                    break
                        
                        opponent_action = strategic_move if strategic_move else random.choice(opponent_moves)
                    else:
                        opponent_action = random.choice(opponent_moves)
                    
                    game.make_move(opponent_action, 'O')
                    next_state = agent.get_state(game.board)
                    
                    if game.current_winner == 'O':
                        reward = -1
                        done = True
                    elif not game.available_moves():
                        done = True
            
            agent.update_q_value(state, action, reward, next_state, done)
            state = next_state
            
            if done:
                break
        
        # More aggressive epsilon decay for better exploration
        if episode % 500 == 0:
            agent.epsilon = max(agent.epsilon * 0.99, 0.005)
        
        # Add some randomness occasionally to explore new states
        if episode % 10000 == 0 and episode > 0:
            agent.epsilon = min(agent.epsilon + 0.02, 0.15)  # Temporary exploration boost
    
    return agent

class RLGameEngine:
    def __init__(self):
        self.game = TicTacToe()
        self.agent = QLearningAgent.load_model('models/trained_agent.pkl')
        self.is_trained = os.path.exists('models/trained_agent.pkl')

    def train_agent(self, episodes=10000):
        """Train the agent"""
        print(f"Training agent for {episodes} episodes...")
        self.agent = train_agent(episodes)
        self.agent.save_model('models/trained_agent.pkl')
        self.is_trained = True
        return {
            "episodes": episodes,
            "q_table_size": len(self.agent.q_table),
            "epsilon": self.agent.epsilon,
            "status": "Training completed"
        }

    def make_move(self, position):
        """Player makes move, AI responds"""
        if position not in self.game.available_moves():
            return {"error": "Invalid move"}
        
        # Player move (X)
        self.game.make_move(position, 'X')
        
        # Check if game over
        if self.game.current_winner or not self.game.available_moves():
            return self.get_game_state()
        
        # AI move (O)
        state = self.agent.get_state(self.game.board)
        available_moves = self.game.available_moves()
        
        if available_moves:
            ai_move = self.agent.choose_action(state, available_moves)
            self.game.make_move(ai_move, 'O')
        
        return self.get_game_state()

    def get_game_state(self):
        return {
            "board": self.game.board,
            "winner": self.game.current_winner,
            "game_over": self.game.current_winner is not None or not self.game.available_moves(),
            "available_moves": self.game.available_moves(),
            "is_trained": self.is_trained
        }

    def reset_game(self):
        self.game.reset()
        return self.get_game_state()