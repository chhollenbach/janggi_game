# Author: Connor Hollenbach
# Date: 2/22/2021
# A program that implements Classes to play the board game "Janggi" aka Korean chess

class GameBoard:
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
        for col in range(len(display_list)):
            for row in display_list:
                print(row[col], end=' ')
            print()


class JanggiGame:
    def __init__(self):
        """Initialize game. Sets up board and places pieces."""
        self._game_state = 'UNFINISHED'
        self._janggi_board = GameBoard()
        self._player_turn = 'b'

    def get_game_state(self):
        """Return state of the game. Can be 'UNFINISHED', 'BLUE_WON', or 'RED_WON' """
        return self._game_state

    def get_janggi_board(self):
        """Return instance of GameBoard for the game (aka _janggi_board object)"""
        return self._janggi_board

    def get_player_turn(self):
        """Return player turn"""
        return self._player_turn

    def change_turn(self):
        """Change player_turn"""
        if self.get_player_turn() == 'b':
            self._player_turn = 'r'
        else:
            self._player_turn = 'b'

    def place_piece(self, location, piece):
        """Places a GamePiece object on the board at a given location. Used to set up game"""
        # Convert string location (e.g. 'b3') to column and row
        col = location[0]
        row = int(location[1:]) - 1
        self._janggi_board.get_board()[col][row] = piece
        return True

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
    def __init__(self, team):
        """Initialize GamePiece object with team (string) of piece"""
        self._team = team

    def get_team(self):
        """Return team of GamePiece"""
        return self._team


class General(GamePiece):
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return "GN"


class Guard(GamePiece):
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return "GD"


class Horse(GamePiece):
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return "HS"


class Elephant(GamePiece):
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return "EL"


class Chariot(GamePiece):
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return "CH"


class Cannon(GamePiece):
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return "CA"


class Soldier(GamePiece):
    def __init__(self, team):
        super().__init__(team)

    def __str__(self):
        return "SD"


def main():
    """Main function to test out code"""
    game = JanggiGame()
    piece1 = Elephant('b')
    game.place_piece('b1', piece1)
    game.get_janggi_board().display_board()


if __name__ == '__main__':
    main()
