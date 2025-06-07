import random

class TicTacToe4x4:
    def __init__(self):
        self.board = [' '] * 16  # 4x4 board represented as a list
        self.current_winner = None
        self.initialize_special_cells()

    def initialize_special_cells(self):
        # **Value-added code: Randomly designate 1 to 4 cells as "both-O-and-X" at the start**
        num_special_cells = random.randint(1, 4)
        special_cells = random.sample(range(16), num_special_cells)
        for cell in special_cells:
            self.board[cell] = 'F'

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
            if self.check_win(square, letter):
                self.current_winner = letter  # Update the winner
            return True
        return False

    def check_win(self, square, letter):
        # **Value-added code: Check for a win condition (4 in a row) including special cells**
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

class AITacAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}  # Q-table for storing state-action values
        self.alpha = alpha   # Learning rate
        self.gamma = gamma   # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.last_state = None
        self.last_action = None

    def get_state(self, board):
        return tuple(board)

    def choose_action(self, state, available_actions):
        if random.uniform(0, 1) < self.epsilon:
            # Explore: select a random action
            action = random.choice(available_actions)
        else:
            # Exploit: select the action with max Q-value
            q_values = [self.q_table.get((state, a), 0) for a in available_actions]
            max_q = max(q_values) if q_values else 0
            # If multiple actions have the same max Q-value, choose one randomly
            max_actions = [a for a, q in zip(available_actions, q_values) if q == max_q]
            action = random.choice(max_actions) if max_actions else random.choice(available_actions)
        # Save the state and action for updating Q-value later
        self.last_state = state
        self.last_action = action
        return action

    def update_q_value(self, reward, next_state, done):
        state = self.last_state
        action = self.last_action
        old_value = self.q_table.get((state, action), 0)
        if not done:
            next_available_actions = [i for i, spot in enumerate(next_state) if spot == ' ']
            future_q_values = [self.q_table.get((next_state, a), 0) for a in next_available_actions]
            future_reward = max(future_q_values) if future_q_values else 0
        else:
            future_reward = 0
        # Q-learning formula
        new_value = old_value + self.alpha * (reward + self.gamma * future_reward - old_value)
        self.q_table[(state, action)] = new_value

def train_agent(episodes):
    agent = AITacAgent()
    for episode in range(episodes):
        game = TicTacToe4x4()
        state = agent.get_state(game.board)
        while True:
            # Agent's turn
            available_moves = game.available_moves()
            if not available_moves:
                break
            action = agent.choose_action(state, available_moves)
            game.make_move(action, 'X')
            next_state = agent.get_state(game.board)
            reward = 0
            done = False
            if game.current_winner == 'X':
                reward = 1  # Agent wins
                done = True
            elif not game.empty_squares():
                reward = 0.5  # Draw
                done = True
            else:
                # Opponent's turn (random move)
                opponent_available_moves = game.available_moves()
                if opponent_available_moves:
                    opponent_action = random.choice(opponent_available_moves)
                    game.make_move(opponent_action, 'O')
                    if game.current_winner == 'O':
                        reward = -1  # Agent loses
                        done = True
                    elif not game.empty_squares():
                        reward = 0.5  # Draw
                        done = True
            # **Value-added code: Update Q-value after each move**
            agent.update_q_value(reward, next_state, done)
            state = next_state
            if done:
                break
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
        state = agent.get_state(game.board)
        available_moves = game.available_moves()
        if not available_moves:
            print('No more moves available. It\'s a tie!')
            return
        action = agent.choose_action(state, available_moves)
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
    # **Value-added code: Increased training episodes for the 4x4 game**
    print('Training AITac for 4x4 Tic-Tac-Toe...')
    trained_agent = train_agent(500000)
    print('Training completed.\nNow you can play against AITac.')
    # Play against the trained agent
    play_against_agent(trained_agent)
