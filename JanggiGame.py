# Author: Connor Hollenbach
# Date: 2/22/2021
# A program that implements Classes to play the board game "Janggi" aka Korean chess

# Using external package to add color to terminal print in order to see red/blue side better
# Remove/comment out before uploading to gradescope?
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

    def get_blue_palace(self):
        """Return list of blue palace squares"""
        return self._blue_palace

    def get_red_palace(self):
        """Return list of red palace squares"""
        return self._red_palace

    def display_board(self):
        """Converts dict of lists to list of lists for accurate display of board"""
        display_list = []
        # Sort key values alphabetically into a list of lists
        for key, value in sorted(self._board.items()):
            display_list.append(value)

        # Print out list of lists vertically
        for col in range(10):
            for row in display_list:
                print(row[col], end=' ')
            print()


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
        pass

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
            return True
        # otherwise, move piece, set old square as 0
        else:
            self._janggi_board.get_board()[b_col][b_row] = self._janggi_board.get_board()[a_col][a_row]
            self._janggi_board.get_board()[a_col][a_row] = '__'

        # TODO: Check for game_state change, remove any capture pieces (done via other methods)

        # Change the turn
        self.change_turn()

        return True


class GamePiece:
    """Generic GamePiece class, tracks the team of a piece"""
    def __init__(self, team):
        """Initialize GamePiece object with team (string) of piece"""
        self._team = team

    def get_team(self):
        """Return team of GamePiece"""
        return self._team


class General(GamePiece):
    """General Class. Can move 1 space in any direction within the palace. Goal is to checkmate the enemy General"""
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return colored("GN", self._team)


class Guard(GamePiece):
    """Guard Piece, can move 1 space in any direction within the palace"""
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return colored("GD", self._team)


class Horse(GamePiece):
    """
    Horse piece, can move one step orthogonally and one step outward (exactly like a horse in Western chess). Cannot
    jump units.
    """
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return colored("HS", self._team)


class Elephant(GamePiece):
    """Elephant piece, moves one step orthogonally and then two steps diagonally. Block by pieces, cannot jump."""
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return colored("EL", self._team)


class Chariot(GamePiece):
    """Chariot piece, moves in straight line, can move diagonally within palace"""
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return colored("CH", self._team)


class Cannon(GamePiece):
    """
    Cannon piece. The cannon can move any number of spaces in a line, so long as it jumps one piece to do so. The jumped
    piece can be friendly or enemy. The jumped piece cannot be another cannon.
    """
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return colored("CA", self._team)


class Soldier(GamePiece):
    """
    Soldier piece. The Solider can move forward or sideways, but not backwards
    """
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return colored("SD", self._team)


def main():
    """Main function to test out code"""
    game = JanggiGame()
    game.get_janggi_board().display_board()


if __name__ == '__main__':
    main()
