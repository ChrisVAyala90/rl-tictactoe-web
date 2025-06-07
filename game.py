import random

class TicTacToe:
    def __init__(self):
        # Initialize a 3x3 board represented as a list
        self.board = [' ']*9  # 3x3 board
        self.current_winner = None  # Keep track of the winner!

    def print_board(self):
        # Prints the current board state
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print()

    def print_board_nums(self):
        # Prints the board with numbers to indicate positions
        number_board = [str(i) for i in range(9)]
        for row in [number_board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print()

    def available_moves(self):
        # Returns a list of indices for empty cells where a move can be made
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        # Returns boolean indicating if there are empty squares on the board
        return ' ' in self.board

    def num_empty_squares(self):
        # Returns the number of empty squares
        return self.board.count(' ')

    def make_move(self, square, letter):
        # Places a move on the board if the chosen square is empty
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter  # Update the winner
            return True
        return False

    def winner(self, square, letter):
        # Check if there's a winner after the last move
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        # Check diagonals
        if square % 2 == 0:
            # Only even squares are part of diagonals
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # Top-left to bottom-right
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # Top-right to bottom-left
            if all([s == letter for s in diagonal2]):
                return True

        return False

class AITacAgent:
    def __init__(self):
        self.q_table = {}  # Q-table mapping (state, action) pairs to Q-values
        self.alpha = 0.1   # Learning rate
        self.gamma = 0.9   # Discount factor for future rewards
        self.epsilon = 0.1 # Exploration rate for the epsilon-greedy strategy

    def get_state(self, board):
        # Converts the board list into a tuple to be used as a key in the Q-table
        return tuple(board)

    def choose_action(self, state, available_actions):
        # Chooses an action based on the epsilon-greedy policy
        if random.uniform(0, 1) < self.epsilon:
            # Explore: select a random action
            return random.choice(available_actions)
        else:
            # Exploit: select the action with the highest Q-value
            q_values = [self.q_table.get((state, a), 0) for a in available_actions]
            max_q = max(q_values)
            # If multiple actions have the same max Q-value, select one at random
            max_actions = [a for a, q in zip(available_actions, q_values) if q == max_q]
            return random.choice(max_actions)

    def update_q_value(self, state, action, reward, next_state, done):
        # Updates the Q-value for a given state-action pair using the Q-learning formula
        old_value = self.q_table.get((state, action), 0)
        future_reward = 0
        if not done:
            # Estimate future rewards from the next state
            next_available_actions = [i for i in range(9) if next_state[i] == ' ']
            if next_available_actions:
                future_q_values = [self.q_table.get((next_state, a), 0) for a in next_available_actions]
                future_reward = max(future_q_values)
        # Q-learning update rule
        new_value = old_value + self.alpha * (reward + self.gamma * future_reward - old_value)
        self.q_table[(state, action)] = new_value

def train_agent(episodes):
    agent = AITacAgent()
    for episode in range(episodes):
        game = TicTacToe()
        state = agent.get_state(game.board)
        while True:
            # Agent's turn
            available_moves = game.available_moves()
            action = agent.choose_action(state, available_moves)
            game.make_move(action, 'X')
            next_state = agent.get_state(game.board)
            reward = 0
            done = False

            if game.current_winner == 'X':
                reward = 1  # Agent wins
                done = True
            elif not game.available_moves():
                done = True  # Draw
            else:
                # Opponent's turn (random move)
                opponent_action = random.choice(game.available_moves())
                game.make_move(opponent_action, 'O')
                next_state = agent.get_state(game.board)

                if game.current_winner == 'O':
                    reward = -1  # Agent loses
                    done = True
                elif not game.available_moves():
                    done = True  # Draw

            # Update Q-value
            agent.update_q_value(state, action, reward, next_state, done)
            state = next_state

            if done:
                break
    return agent

def play_game(agent):
    game = TicTacToe()
    game.print_board_nums()
    while True:
        # Agent's move
        state = agent.get_state(game.board)
        available_moves = game.available_moves()
        action = agent.choose_action(state, available_moves)
        game.make_move(action, 'X')
        print("AITac's Move:")
        game.print_board()

        if game.current_winner == 'X':
            print("AITac wins!")
            break
        elif not game.available_moves():
            print("It's a draw!")
            break

        # Human's move
        valid_square = False
        while not valid_square:
            try:
                human_move = int(input("Your move (0-8): "))
                if human_move not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid move. Try again.")
        game.make_move(human_move, 'O')
        print("Your Move:")
        game.print_board()

        if game.current_winner == 'O':
            print("You win!")
            break
        elif not game.available_moves():
            print("It's a draw!")
            break

# Train the agent over a specified number of episodes
trained_agent = train_agent(500000)

# Play a game against the trained agent
play_game(trained_agent)
