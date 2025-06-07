import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Game environment
class TicTacToe4x4:
    def __init__(self):
        self.board = [' '] * 16  # 4x4 board represented as a list
        self.current_winner = None
        self.special_cells = []
        self.initialize_special_cells()

    def initialize_special_cells(self):
        # Randomly designate 1 to 4 cells as "both-O-and-X" at the start
        num_special_cells = random.randint(1, 4)
        self.special_cells = random.sample(range(16), num_special_cells)
        for cell in self.special_cells:
            self.board[cell] = 'X/O'

    def print_board(self):
        # Prints the current board state
        for row in [self.board[i*4:(i+1)*4] for i in range(4)]:
            print('| ' + ' | '.join(row) + ' |')
        print()

    @staticmethod
    def print_board_nums():
        # Tells which number corresponds to which spot
        number_board = [[str(i) for i in range(j*4, (j+1)*4)] for j in range(4)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')
        print()

    def available_moves(self):
        # Returns a list of available moves (indices)
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        # Checks if there are empty squares on the board
        return ' ' in self.board

    def make_move(self, square, letter):
        # Places a move on the board
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_win(letter):
                self.current_winner = letter  # Update the winner
            return True
        return False

    def check_win(self, letter):
        # Check for a win condition (4 in a row) including special cells
        board = self.board
        win_conditions = []

        # Rows
        for i in range(4):
            win_conditions.append(board[i*4:(i+1)*4])
        # Columns
        for i in range(4):
            win_conditions.append([board[i+j*4] for j in range(4)])
        # Diagonals
        win_conditions.append([board[i*5] for i in range(4)])  # Top-left to bottom-right
        win_conditions.append([board[(i+1)*3] for i in range(4)])  # Top-right to bottom-left

        for condition in win_conditions:
            count = 0
            for cell in condition:
                if cell == letter or cell == 'X/O':
                    count += 1
                else:
                    break
            if count == 4:
                return True
        return False

# Function to encode the board state
def encode_board(board):
    encoding = []
    for cell in board:
        if cell == ' ':
            encoding.append(0)
        elif cell == 'X':
            encoding.append(1)
        elif cell == 'O':
            encoding.append(-1)
        elif cell == 'X/O':
            encoding.append(2)
    return np.array(encoding)

# Deep Q-Network Agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size  # Should be 16 for a 4x4 board
        self.action_size = action_size  # Should be 16
        self.memory = []  # Experience replay memory
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.batch_size = 64
        self.model = self._build_model()
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def _build_model(self):
        # Neural network model
        model = nn.Sequential(
            nn.Linear(self.state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, self.action_size)
        )
        return model

    def remember(self, state, action, reward, next_state, done):
        # Store experience in replay memory
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > 5000:
            self.memory.pop(0)

    def act(self, state, available_actions):
        if np.random.rand() <= self.epsilon:
            # Explore: choose a random action from available actions
            return random.choice(available_actions)
        state = torch.FloatTensor(state)
        act_values = self.model(state)
        act_values = act_values.detach().numpy()[0]
        # Mask invalid actions
        masked_values = np.full(self.action_size, -np.inf)
        masked_values[available_actions] = act_values[available_actions]
        return np.argmax(masked_values)

    def replay(self):
        if len(self.memory) < self.batch_size:
            return  # Not enough experiences to train
        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state)
                target = (reward + self.gamma * np.amax(self.model(next_state).detach().numpy()))
            state = torch.FloatTensor(state)
            target_f = self.model(state).detach().numpy()
            target_f[0][action] = target
            target_f = torch.FloatTensor(target_f)
            # Perform a gradient descent step
            self.optimizer.zero_grad()
            outputs = self.model(state)
            loss = self.criterion(outputs, target_f)
            loss.backward()
            self.optimizer.step()
        # Decrease epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def train_agent(episodes):
    agent = DQNAgent(state_size=16, action_size=16)
    for episode in range(episodes):
        game = TicTacToe4x4()
        state = encode_board(game.board)
        state = np.reshape(state, [1, 16])
        done = False
        while not done:
            available_moves = game.available_moves()
            action = agent.act(state, available_moves)
            valid_move = game.make_move(action, 'X')
            if not valid_move:
                # Invalid move shouldn't happen, but handle just in case
                reward = -10
                next_state = state
                done = True
            else:
                if game.current_winner == 'X':
                    reward = 1
                    done = True
                elif not game.empty_squares():
                    reward = 0  # Draw
                    done = True
                else:
                    # Opponent's turn (random move)
                    opponent_available_moves = game.available_moves()
                    if opponent_available_moves:
                        opponent_action = random.choice(opponent_available_moves)
                        game.make_move(opponent_action, 'O')
                        if game.current_winner == 'O':
                            reward = -1
                            done = True
                        elif not game.empty_squares():
                            reward = 0  # Draw
                            done = True
                        else:
                            reward = -0.01
                            if action in game.special_cells:
                                reward += 0.1
                    else:
                        reward = 0  # Draw
                        done = True
                next_state = encode_board(game.board)
                next_state = np.reshape(next_state, [1, 16])
            # Remember the experience
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                break
        # Train the agent after each episode
        agent.replay()
        # Optional: Print progress
        if (episode + 1) % 1000 == 0:
            print(f'Episode {episode + 1}/{episodes} completed.')
    return agent

def play_against_agent(agent):
    game = TicTacToe4x4()
    print('Initial Board:')
    game.print_board()
    TicTacToe4x4.print_board_nums()
    while game.empty_squares():
        # Human player's turn
        available_moves = game.available_moves()
        move = None
        while move not in available_moves:
            try:
                move = int(input('Your turn. Input move (0-15): '))
            except ValueError:
                print('Invalid input. Please enter a number between 0 and 15.')
                continue
            if move not in available_moves:
                print('Invalid move. Try again.')
        game.make_move(move, 'O')
        print('Your move:')
        game.print_board()
        if game.current_winner == 'O':
            print('You win!')
            return
        elif not game.empty_squares():
            print('It\'s a tie!')
            return
        # Agent's turn
        state = encode_board(game.board)
        state = np.reshape(state, [1, 16])
        available_moves = game.available_moves()
        if not available_moves:
            print('No more moves available. It\'s a tie!')
            return
        action = agent.act(state, available_moves)
        game.make_move(action, 'X')
        print(f'AITac moves to position {action}')
        game.print_board()
        if game.current_winner == 'X':
            print('AITac wins!')
            return
        elif not game.empty_squares():
            print('It\'s a tie!')
            return

if __name__ == '__main__':
    # Train the agent
    print('Training AITac for 4x4 Tic-Tac-Toe with special cells...')
    trained_agent = train_agent(5000)  # You can adjust the number of episodes
    print('Training completed.\nNow you can play against AITac.')
    # Play against the trained agent
    play_against_agent(trained_agent)
