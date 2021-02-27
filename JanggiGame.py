# Author: Connor Hollenbach
# Date: 2/22/2021
# A program that implements Classes to play the board game "Janggi" aka Korean chess

# Using external package to add color to terminal print in order to see red/blue side better
# Will Remove/comment out before uploading to gradescope
from termcolor import colored


class GameBoard:
    """
    Class representing an empty gameboard. Can return itself, a list of squares in the palace, and display
    itself in the terminal
    """
    def __init__(self):
        """Init GameBoard Class with board and palace information"""
        self._board = {x: list('__' for _ in range(10)) for x in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')}
        self._blue_palace = ['d10', 'e10', 'f10', 'd9', 'e9', 'f9', 'd8', 'e8', 'f8']
        self._red_palace = ['d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3']

    def get_board(self):
        """Return _board attribute"""
        return self._board

    def get_palace(self, team):
        """Return list of palace squares for a team"""
        if team == 'blue':
            return self._blue_palace
        else:
            return self._red_palace

    def display_board(self):
        """Converts dict of lists to list of lists for accurate display of board"""
        display_list = []
        # Sort key values alphabetically into a list of lists
        for key, value in sorted(self._board.items()):
            display_list.append(value)

        # Print out list of lists vertically with column and row markers
        print('  a  b  c  d  e  f  g  h  i')
        for col in range(10):
            print(col + 1, end = ' ')
            for row in display_list:
                print(row[col], end = ' ')
            print()

    def get_square(self, location):
        """Return a specific square on the board"""
        col = location[0]
        row = int(location[1:]) - 1
        # if square is off board, return None
        try:
            return_square = self._board[col][row]
        except (KeyError, IndexError):
            return_square = None
        return return_square


class JanggiGame:
    """Class implementation of Janggi. Drives gameplay, links together the GameBoard and GamePiece classes"""
    def __init__(self):
        """Initialize game. Sets up board and places pieces."""
        # Create Data Members
        self._game_state = 'UNFINISHED'
        self._janggi_board = GameBoard()
        self._player_turn = 'blue'

        # Set up pieces of board - PROBABLY CAN FIGURE OUT A BETTER WAY TO SET THIS UP THAN HARD CODING ALL THIS
        # General
        self.place_piece('e2', General('red'))
        self.place_piece('e9', General('blue'))
        # Guard
        self.place_piece('d1', Guard('red'))
        self.place_piece('f1', Guard('red'))
        self.place_piece('d10', Guard('blue'))
        self.place_piece('f10', Guard('blue'))
        # Horse
        self.place_piece('c1', Horse('red'))
        self.place_piece('h1', Horse('red'))
        self.place_piece('c10', Horse('blue'))
        self.place_piece('h10', Horse('blue'))
        # Elephant
        self.place_piece('b1', Elephant('red'))
        self.place_piece('g1', Elephant('red'))
        self.place_piece('b10', Elephant('blue'))
        self.place_piece('g10', Elephant('blue'))
        # Chariot
        self.place_piece('a1', Chariot('red'))
        self.place_piece('i1', Chariot('red'))
        self.place_piece('a10', Chariot('blue'))
        self.place_piece('i10', Chariot('blue'))
        # Cannon
        self.place_piece('b3', Cannon('red'))
        self.place_piece('h3', Cannon('red'))
        self.place_piece('b8', Cannon('blue'))
        self.place_piece('h8', Cannon('blue'))
        # Soldier
        self.place_piece('a4', Soldier('red'))
        self.place_piece('c4', Soldier('red'))
        self.place_piece('e4', Soldier('red'))
        self.place_piece('g4', Soldier('red'))
        self.place_piece('i4', Soldier('red'))
        self.place_piece('a7', Soldier('blue'))
        self.place_piece('c7', Soldier('blue'))
        self.place_piece('e7', Soldier('blue'))
        self.place_piece('g7', Soldier('blue'))
        self.place_piece('i7', Soldier('blue'))

    def place_piece(self, location, piece):
        """Places a GamePiece object on the board at a given location. Used to set up game"""
        # Convert string location (e.g. 'b3') to column and row
        col = location[0]
        row = int(location[1:]) - 1
        self._janggi_board.get_board()[col][row] = piece

    def get_game_state(self):
        """Return state of the game. Can be 'UNFINISHED', 'blue'_WON', or 'RED_WON' """
        return self._game_state

    def get_janggi_board(self):
        """Return instance of GameBoard for the game (aka _janggi_board object)"""
        return self._janggi_board

    def get_player_turn(self):
        """Return player turn"""
        return self._player_turn

    def change_turn(self):
        """Change player_turn"""
        if self.get_player_turn() == 'blue':
            self._player_turn = 'red'
        else:
            self._player_turn = 'blue'

    def remove_piece(self, location):
        """Remove a piece at a location. Used during capturing process"""
        # Convert string location (e.g. 'b3') to column and row
        col = location[0]
        row = int(location[1:]) - 1
        self._janggi_board.get_board()[col][row] = '__'

    def is_in_check(self, team):
        """If the given team is in check, returns True, otherwise return False"""
        pass

    def make_move(self, location_a, location_b):
        """Move a piece from location a to location b"""
        # Convert string locations (e.g. 'b3') to column and row
        a_col = location_a[0]
        a_row = int(location_a[1:]) - 1
        b_col = location_b[0]
        b_row = int(location_b[1:]) - 1

        # TODO: Check if move is valid

        # If locations are the same, turn is passed
        if location_a == location_b:
            self.change_turn()
            return True
        # otherwise, move piece, set old square as 0
        else:
            self._janggi_board.get_board()[b_col][b_row] = self._janggi_board.get_board()[a_col][a_row]
            self._janggi_board.get_board()[a_col][a_row] = '__'

        # TODO: Check for game_state change, remove any capture pieces (done via other methods)

        # Change the turn
        self.change_turn()

        return True

# TODO add return method for pieces that returns the diff of all squares able to move to


class GamePiece:
    """Generic GamePiece class, tracks the team of a piece"""
    def __init__(self, team):
        """Initialize GamePiece object with team (string) of piece and a piece type"""
        self._team = team
        self._type = None

    def get_team(self):
        """Return team of GamePiece"""
        return self._team

    def get_type(self):
        """Return type of GamePiece"""
        return self._type


class General(GamePiece):
    """General Class. Can move 1 space in any direction within the palace. Goal is to checkmate the enemy General"""
    def __init__(self, team):
        """Init General with new type"""
        super().__init__(team)
        self._type = "General"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        return colored("GN", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])
        palace_squares = gameboard.get_palace(self.get_team())

        # Create initial 9 possible moves
        for row_delta in [-1, 0, 1]:
            for col_delta in [-1, 0, 1]:
                move_location = chr(ord(starting_col) + col_delta) + str(starting_row + row_delta)
                # move must be in palace and square must be empty not occupied by enemy
                if move_location in palace_squares and (
                        gameboard.get_square(move_location) == '__' or
                        gameboard.get_square(move_location).get_team() != self.get_team()):
                    move_list.append(chr(ord(starting_col) + col_delta) + str(starting_row + row_delta))

        return set(move_list)


class Guard(GamePiece):
    """Guard Piece, can move 1 space in any direction within the palace"""
    def __init__(self, team):
        """Init Guard with new type"""
        super().__init__(team)
        self._type = "Guard"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        return colored("GD", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])
        palace_squares = gameboard.get_palace(self.get_team())

        # Create initial 9 possible moves
        for row_delta in [-1, 0, 1]:
            for col_delta in [-1, 0, 1]:
                move_location = chr(ord(starting_col) + col_delta) + str(starting_row + row_delta)
                # move must be in palace and square must be empty not occupied by enemy
                if move_location in palace_squares and (
                        gameboard.get_square(move_location) == '__' or
                        gameboard.get_square(move_location).get_team() != self.get_team()):
                    move_list.append(chr(ord(starting_col) + col_delta) + str(starting_row + row_delta))

        return set(move_list)


class Horse(GamePiece):
    """
    Horse piece, can move one step orthogonally and one step outward (exactly like a horse in Western chess). Cannot
    jump units.
    """
    def __init__(self, team):
        """Init Horse with new type"""
        super().__init__(team)
        self._type = "Horse"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        return colored("HS", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])

        # Create 8 possible moves
        # Test if orthogonal square is empty, then test if diagonal square is empty or enemy occupied
        # Right
        if gameboard.get_square(chr(ord(starting_col) + 1) + str(starting_row)) == '__':
            move_1 = chr(ord(starting_col) + 2) + str(starting_row + 1)
            move_2 = chr(ord(starting_col) + 2) + str(starting_row - 1)
            if gameboard.get_square(move_1) is not None and (
                    gameboard.get_square(move_1) == '__' or
                    gameboard.get_square(move_1).get_team() != self.get_team()):
                move_list.append(move_1)
            if gameboard.get_square(move_1) is not None and (
                    gameboard.get_square(move_2) == '__' or
                    gameboard.get_square(move_2).get_team() != self.get_team()):
                move_list.append(move_2)

        # Left
        if gameboard.get_square(chr(ord(starting_col) - 1) + str(starting_row)) == '__':
            move_1 = chr(ord(starting_col) - 2) + str(starting_row + 1)
            move_2 = chr(ord(starting_col) - 2) + str(starting_row - 1)
            if gameboard.get_square(move_1) is not None and (
                    gameboard.get_square(move_1) == '__' or
                    gameboard.get_square(move_1).get_team() != self.get_team()):
                move_list.append(move_1)
            if gameboard.get_square(move_1) is not None and (
                    gameboard.get_square(move_2) == '__' or
                    gameboard.get_square(move_2).get_team() != self.get_team()):
                move_list.append(move_2)

        # Up
        if gameboard.get_square(chr(ord(starting_col)) + str(starting_row + 1)) == '__':
            move_1 = chr(ord(starting_col) + 1) + str(starting_row + 2)
            move_2 = chr(ord(starting_col) - 1) + str(starting_row + 2)
            if gameboard.get_square(move_1) is not None and (
                    gameboard.get_square(move_1) == '__' or
                    gameboard.get_square(move_1).get_team() != self.get_team()):
                move_list.append(move_1)
            if gameboard.get_square(move_1) is not None and (
                    gameboard.get_square(move_2) == '__' or
                    gameboard.get_square(move_2).get_team() != self.get_team()):
                move_list.append(move_2)

        # Down
        if gameboard.get_square(chr(ord(starting_col)) + str(starting_row - 1)) == '__':
            move_1 = chr(ord(starting_col) + 1) + str(starting_row - 2)
            move_2 = chr(ord(starting_col) - 1) + str(starting_row - 2)
            if gameboard.get_square(move_1) is not None and (
                    gameboard.get_square(move_1) == '__' or
                    gameboard.get_square(move_1).get_team() != self.get_team()):
                move_list.append(move_1)
            if gameboard.get_square(move_1) is not None and (
                    gameboard.get_square(move_2) == '__' or
                    gameboard.get_square(move_2).get_team() != self.get_team()):
                move_list.append(move_2)

        return set(move_list)


class Elephant(GamePiece):
    """Elephant piece, moves one step orthogonally and then two steps diagonally. Blocked by pieces, cannot jump."""
    def __init__(self, team):
        """Init Elephant with new type"""
        super().__init__(team)
        self._type = "Elephant"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        return colored("EL", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])

        # Create 8 possible moves
        # Test if orthogonal square is empty, then test if diagonal square is empty or enemy occupied
        # Nested if statements walk through movement to insure no piece is blocking path
        # Movement is one step orthogonally, then one step diagonally out, then one more step diagonally out
        # Right
        if gameboard.get_square(chr(ord(starting_col) + 1) + str(starting_row)) == '__':
            if gameboard.get_square(chr(ord(starting_col) + 2) + str(starting_row + 1)) == '__':
                move = chr(ord(starting_col) + 3) + str(starting_row + 2)
                if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                    move_list.append(move)
            if gameboard.get_square(chr(ord(starting_col) + 2) + str(starting_row - 1)) == '__':
                move = chr(ord(starting_col) + 3) + str(starting_row - 2)
                if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                    move_list.append(move)

        # Left
        if gameboard.get_square(chr(ord(starting_col) - 1) + str(starting_row)) == '__':
            if gameboard.get_square(chr(ord(starting_col) - 2) + str(starting_row + 1)) == '__':
                move = chr(ord(starting_col) - 3) + str(starting_row + 2)
                if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                    move_list.append(move)
            if gameboard.get_square(chr(ord(starting_col) - 2) + str(starting_row - 1)) == '__':
                move = chr(ord(starting_col) - 3) + str(starting_row - 2)
                if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                    move_list.append(move)

        # Up
        if gameboard.get_square(chr(ord(starting_col)) + str(starting_row + 1)) == '__':
            if gameboard.get_square(chr(ord(starting_col) + 1) + str(starting_row + 2)) == '__':
                move = chr(ord(starting_col) + 2) + str(starting_row + 3)
                if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                    move_list.append(move)
            if gameboard.get_square(chr(ord(starting_col) - 1) + str(starting_row + 2)) == '__':
                move = chr(ord(starting_col) - 2) + str(starting_row - 3)
                if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                    move_list.append(move)

        # Down
        if gameboard.get_square(chr(ord(starting_col)) + str(starting_row - 1)) == '__':
            if gameboard.get_square(chr(ord(starting_col) + 1) + str(starting_row - 2)) == '__':
                move = chr(ord(starting_col) + 2) + str(starting_row - 3)
                if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                    move_list.append(move)
            if gameboard.get_square(chr(ord(starting_col) - 1) + str(starting_row - 2)) == '__':
                move = chr(ord(starting_col) - 2) + str(starting_row - 3)
                if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                    move_list.append(move)

        return set(move_list)


class Chariot(GamePiece):
    """Chariot piece, moves in straight line, can move diagonally within palace"""
    def __init__(self, team):
        """Init Chariot with new type"""
        super().__init__(team)
        self._type = "Chariot"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        return colored("CH", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        pass


class Cannon(GamePiece):
    """
    Cannon piece. The cannon can move any number of spaces in a line, so long as it jumps one piece to do so. The jumped
    piece can be friendly or enemy. The jumped piece cannot be another cannon.
    """
    def __init__(self, team):
        """Init Cannon with new type"""
        super().__init__(team)
        self._type = "Cannon"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        return colored("CA", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        pass


class Soldier(GamePiece):
    """
    Soldier piece. The Solider can move forward or sideways, but not backwards
    """
    def __init__(self, team):
        """Init Soldier with new type"""
        super().__init__(team)
        self._type = "Soldier"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        return colored("SD", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])

        # Create 3 possible moves, forward movement depending on team
        move_sideways_1 = chr(ord(starting_col) - 1) + str(starting_row)
        move_sidweays_2 = chr(ord(starting_col) + 1) + str(starting_row)
        if self.get_team() == 'blue':
            move_forward = chr(ord(starting_col)) + str(starting_row - 1)
        else:
            move_forward = chr(ord(starting_col)) + str(starting_row + 1)

        # check that move is not off the board/onto a friendly piece
        for move in [move_sideways_1, move_sidweays_2, move_forward]:
            if gameboard.get_square(move) is not None and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                move_list.append(move)

        return set(move_list)


def main():
    """Main function to test out code"""
    game = JanggiGame()
    game.get_janggi_board().display_board()
    # Test movement
    board = game.get_janggi_board()
    print(game.get_janggi_board().get_square('a4').valid_moves('a4', board))


if __name__ == '__main__':
    main()
