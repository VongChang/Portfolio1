import math
import random

class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(16)]

    def print_board(self):
        for row in [self.board[i * 4:(i + 1) * 4] for i in range(4)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():  # 0 | 4 | 8 | 12
        number_board = [[str(i) for i in range(j * 4, (j + 1) * 4)] for j in range(4)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check the Row
        row_ind = math.floor(square / 4)
        row = self.board[row_ind * 4:(row_ind + 1) * 4]
        if all([s == letter for s in row]):
            return True

        col_ind = square % 4
        column = self.board[col_ind::4]  # Corrected this line
        if all([s == letter for s in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 5, 10, 15]]
            if all(s == letter for s in diagonal1):
                return True
            diagonal2 = [self.board[i] for i in [3, 6, 9, 12]]
            if all(s == letter for s in diagonal2):
                return True
        return False

    def empty_square(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_move(self):
        return [i for i, x in enumerate(self.board) if x == " "]

class Player():
    def __init__(self, letter):
        self.letter = letter
    
    def get_move(self, game):
        pass

class HumanUser(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-15): ')
            try:
                val = int(square)
                if val not in game.available_move():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again.")
        return val
    
class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_move())
        return square 
    
class SmartAIPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        if len(game.available_move()) == 16:
            square = random.choice(game.available_move())
        else:
            square = self.minimax(game, self.letter)['position']
        return square 
    
    def minimax(self, state, player, alpha=-math.inf, beta=math.inf):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * state.num_empty_squares() if other_player == max_player else -1 * state.num_empty_squares()}
        elif not state.empty_square():
            return {'position': None, 'score': 0}
        
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
            for possible_move in state.available_move():
                state.make_move(possible_move, player)
                sim_score = self.minimax(state, other_player, alpha, beta)
                state.board[possible_move] = ' '
                state.current_winner = None
                sim_score['position'] = possible_move
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, best['score'])
                if beta <= alpha:
                    break  # Beta cutoff
        else:
            best = {'position': None, 'score': math.inf}
            for possible_move in state.available_move():
                state.make_move(possible_move, player)
                sim_score = self.minimax(state, other_player, alpha, beta)
                state.board[possible_move] = ' '
                state.current_winner = None
                sim_score['position'] = possible_move
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, best['score'])
                if beta <= alpha:
                    break  # Alpha cutoff
        return best

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()
    
    letter = 'X'
    while game.empty_square():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):
            
            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board()
                print('')
            
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter
            letter = 'O' if letter == 'X' else 'X'
    
    if print_game:
        print('It\'s a tie')

if __name__ == '__main__':
    x_player = SmartAIPlayer('X')
    o_player = HumanUser('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)