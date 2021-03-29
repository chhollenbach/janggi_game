# Author: Connor Hollenbach
# Date: 2/22/2021
# A program that implements Classes to play the board game "Janggi" aka Korean chess

from termcolor import colored
import pygame
import os
import random


class GameBoard:
    """
    Class representing an empty gameboard. The Gameboard is a dict of lists, and holds the various pieces in the game.
    This class will not directly call/interact with any other classes, although GamePiece classes will be stored
    in the various squares.
    """
    def __init__(self):
        """Init GameBoard Class with board and palace information. The board is a dict of lists."""
        self._board = {x: list('__' for _ in range(10)) for x in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')}
        self._blue_palace = ['d10', 'e10', 'f10', 'd9', 'e9', 'f9', 'd8', 'e8', 'f8']
        self._red_palace = ['d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3']
        self._blue_diag_palace = ['d10', 'f10', 'e9', 'd8', 'f8']
        self._red_diag_palace = ['d1', 'f1', 'e2', 'd3', 'f3']

    def get_board(self):
        """Return the board, which is a dict of lists"""
        return self._board

    def get_palace(self, team):
        """Return list of palace squares for an input team. Palaces squares are string locations"""
        if team == 'blue':
            return self._blue_palace
        else:
            return self._red_palace

    def get_both_palaces(self):
        """Return list of all palace squares on the board. Palaces squares are string locations"""
        all_palace_squares = self._red_palace + self._blue_palace
        return all_palace_squares

    def get_team_diag_palace(self, team):
        """Return a list of string palace squares from which diagonal moves can be made for a given team."""
        if team == 'blue':
            return self._blue_diag_palace
        else:
            return self._red_diag_palace

    def get_both_diag_palace(self):
        """Return a list of string palace squares from which diagonal moves can be made for both palaces."""
        return self._red_diag_palace + self._blue_diag_palace

    def display_board(self):
        """Converts dict of lists to list of lists and prints vertically for accurate display of board in terminal"""
        display_list = []
        # Sort key values alphabetically into a list of lists
        for key, value in sorted(self._board.items()):
            display_list.append(value)

        # Print out list of lists vertically with column and row markers
        print('   a  b  c  d  e  f  g  h  i')
        for col in range(10):
            if col + 1 < 10:
                print(col + 1, end='  ')
            # adjust spacing for double digit row (10)
            else:
                print(col + 1, end=' ')
            for row in display_list:
                print(row[col], end=' ')
            print()

    def get_square(self, location):
        """
        Return a specific square on the board at location (string input). Return value is either a GamePiece, a
        string "__" denoting an empty square, or None, which represents the out of bounds area
        """
        col = location[0]
        row = int(location[1:]) - 1
        # if square is off board, return None
        if row < 0 or row > 9 or col < 'a' or col > 'i':
            return None
        return_square = self._board[col][row]
        return return_square

    def set_square(self, location, value):
        """Set square at location (string input) to value (either empty string or gamepiece)"""
        col = location[0]
        row = int(location[1:]) - 1
        self._board[col][row] = value


class JanggiGame:
    """
    Class implementation of Janggi. Drives gameplay, links together the GameBoard and GamePiece classes. Responsible for
    high level game tasks, like setting the board, moving pieces, checking and changing the game status and player turn
    """
    def __init__(self):
        """Initialize game. Sets up board and places pieces. Tracks game state, board, turn, and general location"""
        # Create Data Members
        self._game_state = 'UNFINISHED'
        self._janggi_board = GameBoard()
        self._player_turn = 'blue'
        self._blue_general = 'e9'
        self._red_general = 'e2'

        # Set up pieces of board - PROBABLY CAN FIGURE OUT A BETTER WAY TO SET THIS UP THAN HARD CODING ALL THIS
        # General
        self._janggi_board.set_square('e2', General('red'))
        self._janggi_board.set_square('e9', General('blue'))
        # Guard
        self._janggi_board.set_square('d1', Guard('red'))
        self._janggi_board.set_square('f1', Guard('red'))
        self._janggi_board.set_square('d10', Guard('blue'))
        self._janggi_board.set_square('f10', Guard('blue'))
        # Horse
        self._janggi_board.set_square('c1', Horse('red'))
        self._janggi_board.set_square('h1', Horse('red'))
        self._janggi_board.set_square('c10', Horse('blue'))
        self._janggi_board.set_square('h10', Horse('blue'))
        # Elephant
        self._janggi_board.set_square('b1', Elephant('red'))
        self._janggi_board.set_square('g1', Elephant('red'))
        self._janggi_board.set_square('b10', Elephant('blue'))
        self._janggi_board.set_square('g10', Elephant('blue'))
        # Chariot
        self._janggi_board.set_square('a1', Chariot('red'))
        self._janggi_board.set_square('i1', Chariot('red'))
        self._janggi_board.set_square('a10', Chariot('blue'))
        self._janggi_board.set_square('i10', Chariot('blue'))
        # Cannon
        self._janggi_board.set_square('b3', Cannon('red'))
        self._janggi_board.set_square('h3', Cannon('red'))
        self._janggi_board.set_square('b8', Cannon('blue'))
        self._janggi_board.set_square('h8', Cannon('blue'))
        # Soldier
        self._janggi_board.set_square('a4', Soldier('red'))
        self._janggi_board.set_square('c4', Soldier('red'))
        self._janggi_board.set_square('e4', Soldier('red'))
        self._janggi_board.set_square('g4', Soldier('red'))
        self._janggi_board.set_square('i4', Soldier('red'))
        self._janggi_board.set_square('a7', Soldier('blue'))
        self._janggi_board.set_square('c7', Soldier('blue'))
        self._janggi_board.set_square('e7', Soldier('blue'))
        self._janggi_board.set_square('g7', Soldier('blue'))
        self._janggi_board.set_square('i7', Soldier('blue'))

    def get_game_state(self):
        """Return state of the game. Can be 'UNFINISHED', 'BLUE'_WON', or 'RED_WON' """
        return self._game_state

    def set_game_state(self, new_game_state):
        """Update the game state with a new_game_state. Expected value is a string for BLUE_WON or RED_WON"""
        self._game_state = new_game_state

    def get_janggi_board(self):
        """Return instance of GameBoard for the game (aka GameBoard object)"""
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

    def change_general_location(self, new_location, team):
        """Update tracking location of general. Used in make_move method. DOES NOT ACTUALLY MOVE GENERAL"""
        if team == 'blue':
            self._blue_general = new_location
        else:
            self._red_general = new_location

    def get_general_loc(self, team):
        """Return location of general for a team"""
        if team == 'blue':
            return self._blue_general
        else:
            return self._red_general

    def get_opposite_team(self):
        """Return the opposite team of the player turn."""
        if self.get_player_turn() == 'red':
            return 'blue'
        else:
            return 'red'

    def are_generals_facing(self):
        """Checks if generals are facing unobstructed and returns True or False"""
        red_general_column = self._red_general[0]
        blue_general_column = self._blue_general[0]
        if red_general_column == blue_general_column:
            red_general_flag = False
            intercepting_piece_flag = False
            # Loop through column of generals, find red general (since red will always come before blue), check if
            # piece is between red and blue general
            for val in self._janggi_board.get_board()[red_general_column]:
                if red_general_flag is True and val != "__" and val.get_type() == "General" and intercepting_piece_flag is False:
                    return True
                if red_general_flag is True and val != "__" and val.get_type() != "General":
                    intercepting_piece_flag = True
                if val != "__" and val.get_type() == "General" and val.get_team() == 'red':
                    red_general_flag = True
        return False

    def get_all_enemy_moves(self, team):
        """
        Determine all possible moves of enemy. Used for check/mate logic. Returns set of all move locations for
        opposing team input. Team input should be a string, 'blue' or 'red'
        """
        enemy_move_set = set()
        for key, value in self._janggi_board.get_board().items():
            row = 1
            for square in value:
                if square != "__" and square.get_team() != team:
                    location = key + str(row)
                    moves = square.valid_moves(location, self.get_janggi_board())
                    enemy_move_set.update(moves)
                row += 1

        return enemy_move_set

    def is_in_check(self, team):
        """If the given team is in check, returns True, otherwise return False"""
        enemy_move_set = self.get_all_enemy_moves(team)
        if team == 'blue' and self._blue_general in enemy_move_set:
            return True
        elif team == 'red' and self._red_general in enemy_move_set:
            return True
        else:
            return False

    def is_in_checkmate(self, team):
        """If a given team is in checkmate, returns True, otherwise returns False"""
        # loop through board. for each ally piece, get moves, try move, check if still in check. if no, revert move
        # and return false. if yes, revert move and continue to next move
        # Loop through key, value of board
        for key, value in self._janggi_board.get_board().items():
            # Keep track of row index
            row = 1
            # square is either "__" or a gamepiece
            for square in value:
                if square != "__" and square.get_team() == team:
                    location = key + str(row)
                    moves = square.valid_moves(location, self.get_janggi_board())
                    # Loop through all moves for a gamepiece
                    for move in moves:
                        # Record contents of move location for roll back
                        new_square_value = self.get_janggi_board().get_square(move)
                        # Move gamepiece to new move location
                        self.get_janggi_board().set_square(move, square)
                        if square.get_type() == "General":
                            self.change_general_location(move, team)
                        # Check if still in check
                        check_value = self.is_in_check(team)
                        # Roll back move
                        self.get_janggi_board().set_square(move, new_square_value)
                        self.get_janggi_board().set_square(location, square)
                        if square.get_type() == "General":
                            self.change_general_location(location, team)
                        if check_value is False:
                            # If not in check, team is not in checkmate. return False
                            return False
                row += 1

        # If every move still leaves team in check, team is in check mate, return True
        return True

    def make_move(self, location_a, location_b):
        """
        Move a piece from location a to location b. Locations are string inputs. Returns False if move is invalid
        but otherwise moves piece, updates gamestate/player turn and returns true.
        """
        # get value at location_a and location_b, and location of general
        # the latter two are used to roll the game back if necessary
        from_square = self._janggi_board.get_square(location_a)
        to_square = self._janggi_board.get_square(location_b)
        general_location = self.get_general_loc(self.get_player_turn())

        # Pass turn if location_a and location_b are the same, and the player isn't in check
        # IN ORIGINAL SPECS THIS WAS USED TO PASS TURN
        # USING PYGAME, BUTTON IS CREATED TO PASS TURN, FEEDING SAME LOCATION WILL JUST RESET MOVE
        # player_in_check_at_beginning_of_turn = self.is_in_check(self._player_turn)
        # if location_a == location_b and player_in_check_at_beginning_of_turn is False:
        #     self.change_turn()
        #     return True
        if location_a == location_b:
            return False

        # Check for validity of move
        # Check that location_a is in game bounds, there is a friendly unit there, and game isn't over
        elif from_square == '__' or from_square is None or from_square.get_team() != self._player_turn or self._game_state != 'UNFINISHED':
            return False
        # check that location_b is in valid moves for unit at location_a
        elif location_b not in from_square.valid_moves(location_a, self.get_janggi_board()):
            return False
        else:
            # Move piece, set old square to empty string
            # Also update location of general if general moved
            if from_square.get_type() == "General":
                self.change_general_location(location_b, self.get_player_turn())
            self._janggi_board.set_square(location_b, from_square)
            self._janggi_board.set_square(location_a, "__")

            # Insure that player does not end their turn in check or with generals facing
            # If the player does end their turn in check, we need to roll the move back and return False
            # A player ends their turn in check if they move into check (invalid) or do not move out of check if placed
            # into it by the enemy in the previous turn
            # We make the move first so that we can check all enemy moves after player move, as player move can effect
            # enemy move possibilities
            player_in_check_after_move = self.is_in_check(self._player_turn)
            generals_facing = self.are_generals_facing()
            if player_in_check_after_move is True or generals_facing is True:
                if from_square.get_type() == "General":
                    self.change_general_location(general_location, self.get_player_turn())
                self._janggi_board.set_square(location_b, to_square)
                self._janggi_board.set_square(location_a, from_square)
                return False

        # If move put opposing player in check, check for check mate
        # If check mate found, update game state and return True
        opposing_player_in_check = self.is_in_check(self.get_opposite_team())
        if opposing_player_in_check is True:
            opposing_player_in_checkmate = self.is_in_checkmate(self.get_opposite_team())
            if opposing_player_in_checkmate is True:
                if self.get_player_turn() == 'red':
                    self.set_game_state('RED_WON')
                else:
                    self.set_game_state('BLUE_WON')
                return True

        # Change the turn and return True to end turn
        self.change_turn()
        return True

    def swap_horse_elephant(self, team, side):
        """
        For a team, takes either 'both', 'left', 'right', 'neither' as side arguments. Swap elephant and horse for chosen
        side. Used in setup before moves are made.
        """
        if side not in ['neither', 'right', 'left', 'both']:
            return False

        if team == 'blue':
            if side == 'neither':
                return True
            elif side == 'right':
                self._janggi_board.set_square('g10', Horse('blue'))
                self._janggi_board.set_square('h10', Elephant('blue'))
            elif side == 'left':
                self._janggi_board.set_square('b10', Horse('blue'))
                self._janggi_board.set_square('c10', Elephant('blue'))
            else:
                self._janggi_board.set_square('b10', Horse('blue'))
                self._janggi_board.set_square('c10', Elephant('blue'))
                self._janggi_board.set_square('g10', Horse('blue'))
                self._janggi_board.set_square('h10', Elephant('blue'))

        if team == 'red':
            if side == 'neither':
                return True
            elif side == 'right':
                self._janggi_board.set_square('g1', Horse('red'))
                self._janggi_board.set_square('h1', Elephant('red'))
            elif side == 'left':
                self._janggi_board.set_square('b1', Horse('red'))
                self._janggi_board.set_square('c1', Elephant('red'))
            else:
                self._janggi_board.set_square('b1', Horse('red'))
                self._janggi_board.set_square('c1', Elephant('red'))
                self._janggi_board.set_square('g1', Horse('red'))
                self._janggi_board.set_square('h1', Elephant('red'))

    def auto_move(self, team):
        """
        VERY rudimentary AI. Simply loops through  all possible moves, and makes a capture if possible, otherwise randomly moves piece
        """
        # define value of pieces
        piece_point_dict = {'General': 900, 'Guard': 20, 'Horse': 50, 'Elephant': 50, 'Chariot': 90, 'Cannon': 50, 'Soldier': 10}

        max_point = 0
        max_move = None
        move_list = []

        # Loop through key, value of board
        for key, value in self._janggi_board.get_board().items():
            # Keep track of row index
            row = 1
            # square is either "__" or a gamepiece
            for square in value:
                if square != "__" and square.get_team() == team:
                    location = key + str(row)
                    moves = square.valid_moves(location, self.get_janggi_board())
                    # Loop through all moves for a gamepiece
                    for move in moves:
                        move_list.append([location, move])
                        move_square = self.get_janggi_board().get_square(move)
                        if move_square != "__" and piece_point_dict[move_square.get_type()] > max_point:
                            max_point = piece_point_dict[move_square.get_type()]
                            max_move = [location, move]
                row += 1

        if max_point > 0:
            return max_move
        else:
            return random.choice(move_list)


class GamePiece:
    """
    Parent GamePiece class, tracks the team and type of a piece. Is inherited by various classes representing the unique
    pieces of Janggi. The child classes will contain the method valid_moves, which will list all spaces that a piece
    can move to legally.
    """
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
    """
    General Class. Can move 1 space in any direction within the palace.
    """
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
        palace_diag_squares = gameboard.get_team_diag_palace(self.get_team())

        # Create initial 9 possible moves
        for row_delta in [-1, 0, 1]:
            for col_delta in [-1, 0, 1]:
                move_location = chr(ord(starting_col) + col_delta) + str(starting_row + row_delta)
                # move must be in palace and square must be empty not occupied by enemy
                if move_location in palace_squares and (
                        gameboard.get_square(move_location) == '__' or
                        gameboard.get_square(move_location).get_team() != self.get_team()):
                    # diagonal moves must by from diagonally connect palace squares
                    if abs(row_delta) + abs(col_delta) == 2:
                        if location in palace_diag_squares:
                            move_list.append(chr(ord(starting_col) + col_delta) + str(starting_row + row_delta))
                    else:
                        move_list.append(chr(ord(starting_col) + col_delta) + str(starting_row + row_delta))

        return set(move_list)


class Guard(GamePiece):
    """
    Guard Clas. Can move 1 space in any direction within the palace.
    """
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
        palace_diag_squares = gameboard.get_team_diag_palace(self.get_team())

        # Create initial 9 possible moves
        for row_delta in [-1, 0, 1]:
            for col_delta in [-1, 0, 1]:
                move_location = chr(ord(starting_col) + col_delta) + str(starting_row + row_delta)
                # move must be in palace and square must be empty not occupied by enemy
                if move_location in palace_squares and (
                        gameboard.get_square(move_location) == '__' or
                        gameboard.get_square(move_location).get_team() != self.get_team()):
                    # diagonal moves must by from diagonally connect palace squares
                    if abs(row_delta) + abs(col_delta) == 2:
                        if location in palace_diag_squares:
                            move_list.append(chr(ord(starting_col) + col_delta) + str(starting_row + row_delta))
                    else:
                        move_list.append(chr(ord(starting_col) + col_delta) + str(starting_row + row_delta))

        return set(move_list)


class Horse(GamePiece):
    """
    Horse Class. Can move one step orthogonally and one step diagonally outward. Cannot jump units.
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
            if gameboard.get_square(move_2) is not None and (
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
            if gameboard.get_square(move_2) is not None and (
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
            if gameboard.get_square(move_2) is not None and (
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
            if gameboard.get_square(move_2) is not None and (
                    gameboard.get_square(move_2) == '__' or
                    gameboard.get_square(move_2).get_team() != self.get_team()):
                move_list.append(move_2)

        return set(move_list)


class Elephant(GamePiece):
    """
    Elephant Class. Moves one step orthogonally and then two steps diagonally outwards. Cannot jump pieces.
    """
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
                move = chr(ord(starting_col) - 2) + str(starting_row + 3)
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
    """
    Chariot Class. Moves in an orthogonal line, and can move diagonally within palace.
    """
    def __init__(self, team):
        """Init Chariot with new type"""
        super().__init__(team)
        self._type = "Chariot"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        return colored("CH", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])
        palace_squares = gameboard.get_both_palaces()
        palace_diag_squares = gameboard.get_both_diag_palace()

        # Chariot moves in 4 orthogonal directions while outside palace, and 8 directions inside palace
        for direction in ['up', 'right', 'down', 'left', 'upright', 'downright', 'downleft', 'upleft']:
            stop_flag = False
            last_col = starting_col
            last_row = starting_row
            # all moves in a line up to edge of board/ally piece/onto enemy piece are valid
            # if in palace, can move diagonally to edge of palace as well
            if direction in ['upright', 'downright', 'downleft', 'upleft'] and location not in palace_diag_squares:
                # if chariot is not in diagonally connect palace squares, it can't move diagonally
                stop_flag = True
            while stop_flag is False:
                if direction == 'up':
                    next_location = chr(ord(last_col)) + str(last_row + 1)
                elif direction == 'right':
                    next_location = chr(ord(last_col) + 1) + str(last_row)
                elif direction == 'down':
                    next_location = chr(ord(last_col)) + str(last_row - 1)
                elif direction == 'left':
                    next_location = chr(ord(last_col) - 1) + str(last_row)
                elif direction == 'upright':
                    next_location = chr(ord(last_col) + 1) + str(last_row + 1)
                elif direction == 'downright':
                    next_location = chr(ord(last_col) + 1) + str(last_row - 1)
                elif direction == 'downleft':
                    next_location = chr(ord(last_col) - 1) + str(last_row - 1)
                else:
                    next_location = chr(ord(last_col) - 1) + str(last_row + 1)
                next_square = gameboard.get_square(next_location)
                # if next square is off board, stop
                if next_square is None:
                    stop_flag = True
                # if moving diagonally, and next square is outside the palace, stop
                elif direction in ['upright', 'downright', 'downleft',
                                   'upleft'] and next_location not in palace_squares:
                    stop_flag = True
                # if next square is empty, can move there
                elif next_square == '__':
                    move_list.append(next_location)
                # if next square is ally, stop
                elif next_square.get_team() == self.get_team():
                    stop_flag = True
                # if next square is enemy, can move there but stop after
                else:
                    move_list.append(next_location)
                    stop_flag = True
                # advance last col/row info to next square for next iteration
                last_col = next_location[0]
                last_row = int(next_location[1:])

        return set(move_list)


class Cannon(GamePiece):
    """
    Cannon Class. The cannon can move any number of spaces in an orthonoal line, so long as it jumps one piece to do so.
    The jumped piece can be friendly or enemy. The jumped piece cannot be another cannon. The cannon cannot capture an
    enemy cannon. The cannon can move diagonally within the palace (like the Chariot)
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
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])
        palace_squares = gameboard.get_both_palaces()
        palace_diag_squares = gameboard.get_both_diag_palace()

        # Cannon moves in 4 orthogonal directions while outside palace, and 8 directions inside palace. It must jump a unit
        for direction in ['up', 'right', 'down', 'left', 'upright', 'downright', 'downleft', 'upleft']:
            stop_flag = False
            unit_counter = 0
            last_col = starting_col
            last_row = starting_row
            # all moves in a line up to edge of board/ally piece/onto enemy piece are valid
            # if in palace, can move diagonally to edge of palace as well
            if direction in ['upright', 'downright', 'downleft', 'upleft'] and location not in palace_diag_squares:
                # if cannon is not in diagonally connected palace squares, it can't move diagonally
                stop_flag = True
            while stop_flag is False:
                # Set next location based on direction
                if direction == 'up':
                    next_location = chr(ord(last_col)) + str(last_row + 1)
                elif direction == 'right':
                    next_location = chr(ord(last_col) + 1) + str(last_row)
                elif direction == 'down':
                    next_location = chr(ord(last_col)) + str(last_row - 1)
                elif direction == 'left':
                    next_location = chr(ord(last_col) - 1) + str(last_row)
                elif direction == 'upright':
                    next_location = chr(ord(last_col) + 1) + str(last_row + 1)
                elif direction == 'downright':
                    next_location = chr(ord(last_col) + 1) + str(last_row - 1)
                elif direction == 'downleft':
                    next_location = chr(ord(last_col) - 1) + str(last_row - 1)
                else:
                    next_location = chr(ord(last_col) - 1) + str(last_row + 1)
                next_square = gameboard.get_square(next_location)

                # add moves to move_list if they are valid
                # if next square is off board, stop
                if next_square is None:
                    stop_flag = True
                # if the next unit is a cannon, stop, cannot jump or capture cannon
                elif next_square != "__" and next_square.get_type() == 'Cannon':
                    stop_flag = True
                # if moving diagonally, and next square is outside the palace, stop
                elif direction in ['upright', 'downright', 'downleft',
                                   'upleft'] and next_location not in palace_squares:
                    stop_flag = True
                # if next square is empty, can move there so long as there is one piece in the way
                elif next_square == '__' and unit_counter == 1:
                    move_list.append(next_location)
                # if next square is empty but we haven't passed a unit, move to next iteration
                # adding this condition so next if condition methods don't get called on strings
                elif next_square == '__' and unit_counter != 1:
                    pass
                # if next square is ally, and we've jumped a unit, stop
                elif next_square.get_team() == self.get_team() and unit_counter == 1:
                    stop_flag = True
                # if next square is enemy, and we've jumped a unit, can move to space and then stop
                elif next_square.get_team() != self.get_team() and unit_counter == 1:
                    move_list.append(next_location)
                    stop_flag = True
                # if next square is unit increment unit counter but don't add space to move pool
                elif next_square is not None and next_square != '__' and next_square.get_type() != 'Cannon':
                    unit_counter += 1

                # advance last col/row info to next square for next iteration
                last_col = next_location[0]
                last_row = int(next_location[1:])

        return set(move_list)


class Soldier(GamePiece):
    """
    Soldier Class. The Solider can move forward or sideways, but not backwards.
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
        # get enemy team palace squares for diagonal movement validation
        team = self.get_team()
        if team == 'red':
            enemy_team = 'blue'
        else:
            enemy_team = 'red'
        palace_squares = gameboard.get_palace(enemy_team)
        palace_diag_squares = gameboard.get_team_diag_palace(enemy_team)

        # Create 5 possible moves, forward movement depending on team
        move_sideways_1 = chr(ord(starting_col) - 1) + str(starting_row)
        move_sidweays_2 = chr(ord(starting_col) + 1) + str(starting_row)
        if self.get_team() == 'blue':
            move_forward = chr(ord(starting_col)) + str(starting_row - 1)
            move_diag_1 = chr(ord(starting_col) + 1) + str(starting_row - 1)
            move_diag_2 = chr(ord(starting_col) - 1) + str(starting_row - 1)
        else:
            move_forward = chr(ord(starting_col)) + str(starting_row + 1)
            move_diag_1 = chr(ord(starting_col) + 1) + str(starting_row + 1)
            move_diag_2 = chr(ord(starting_col) - 1) + str(starting_row + 1)

        # check that move is not off the board/onto a friendly piece
        for move in [move_sideways_1, move_sidweays_2, move_forward]:
            if gameboard.get_square(move) is not None and (
                    gameboard.get_square(move) == '__' or
                    gameboard.get_square(move).get_team() != self.get_team()):
                move_list.append(move)
        # Check diagonal moves for being in the palace and originating from diagonally connected squares
        for move in [move_diag_1, move_diag_2]:
            if gameboard.get_square(
                    move) is not None and move in palace_squares and location in palace_diag_squares and (
                    gameboard.get_square(move) == '__' or gameboard.get_square(move).get_team() != self.get_team()):
                move_list.append(move)

        return set(move_list)


def main():
    """Run game using pygame"""

    # Initialize pygame
    pygame.init()

    # Define screen width/height
    screen_width = 90 * 10
    board_height = 100 * 10
    screen_height = board_height + int(.14 * board_height)

    # Define colors
    board_color = (199, 158, 89)
    red_color = (255, 0, 0)
    blue_color = (0, 43, 198)
    black_color = (0, 0, 0)
    white_color = (255, 255, 255)

    # Define piece dimensions
    piece_width = int(screen_width * 0.10)
    piece_height = int(screen_width * 0.10)

    # Create screen
    screen = pygame.display.set_mode([screen_width, screen_height])

    # Import background image
    bg = pygame.image.load(os.path.join('images', 'empty_board.png'))
    bg_scaled = pygame.transform.scale(bg, (screen_width, board_height))

    # Create surface of same color as board at bottom to extend usable space
    bottom_space = pygame.Surface((screen_width, screen_height - board_height))

    # Create dict to map game location string to screen coord - [col, row]
    board_to_coord_map = {}
    col_counter = 0
    for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
        for row in range(1, 11):
            board_to_coord_map[col + str(row)] = (0.05 * screen_width + .112676 * screen_width * col_counter,
                                                  0.05 * screen_width + .112676 * screen_width * (row-1))
        col_counter += 1

    # Generate list of rectangles to detect clicking
    piece_rect_list = []
    for key, val in board_to_coord_map.items():
        location_rect = pygame.Rect(0, 0, piece_width, piece_height)
        location_rect.center = val
        piece_rect_list.append(location_rect)

    # Create game won font and message font
    pygame.font.init()
    endgame_font = pygame.font.SysFont('Palatino Linotype', 70)
    message_font = pygame.font.SysFont('Palatino Linotype', 20)

    # Load piece images
    red_king = pygame.transform.scale(pygame.image.load(os.path.join('images', 'red_king.png')),
                                      (piece_width, piece_height))
    blue_king = pygame.transform.scale(pygame.image.load(os.path.join('images', 'blue_king.png')),
                                       (piece_width, piece_height))
    red_guard = pygame.transform.scale(pygame.image.load(os.path.join('images', 'red_advisor.png')),
                                       (piece_width, piece_height))
    blue_guard = pygame.transform.scale(pygame.image.load(os.path.join('images', 'blue_advisor.png')),
                                        (piece_width, piece_height))
    red_horse = pygame.transform.scale(pygame.image.load(os.path.join('images', 'red_horse.png')),
                                       (piece_width, piece_height))
    blue_horse = pygame.transform.scale(pygame.image.load(os.path.join('images', 'blue_horse.png')),
                                        (piece_width, piece_height))
    red_elephant = pygame.transform.scale(pygame.image.load(os.path.join('images', 'red_elephant.png')),
                                          (piece_width, piece_height))
    blue_elephant = pygame.transform.scale(pygame.image.load(os.path.join('images', 'blue_elephant.png')),
                                           (piece_width, piece_height))
    red_chariot = pygame.transform.scale(pygame.image.load(os.path.join('images', 'red_chariot.png')),
                                         (piece_width, piece_height))
    blue_chariot = pygame.transform.scale(pygame.image.load(os.path.join('images', 'blue_chariot.png')),
                                          (piece_width, piece_height))
    red_cannon = pygame.transform.scale(pygame.image.load(os.path.join('images', 'red_cannon.png')),
                                        (piece_width, piece_height))
    blue_cannon = pygame.transform.scale(pygame.image.load(os.path.join('images', 'blue_cannon.png')),
                                         (piece_width, piece_height))
    red_soldier = pygame.transform.scale(pygame.image.load(os.path.join('images', 'red_pawn.png')),
                                         (piece_width, piece_height))
    blue_soldier = pygame.transform.scale(pygame.image.load(os.path.join('images', 'blue_pawn.png')),
                                          (piece_width, piece_height))

    # Load skip and surrender buttons
    skip_button = pygame.transform.scale(pygame.image.load(os.path.join('images', 'skip_button.png')), (piece_width, piece_width))
    surrender_button = pygame.transform.scale(pygame.image.load(os.path.join('images', 'surrender_button.png')), (piece_width, piece_width))

    # Generate rectangles to detect clicking of skip and surrender button
    skip_button_rect = skip_button.get_rect()
    skip_button_rect.center = (screen_width * .25, board_height + (screen_height - board_height) * .5)
    surrender_button_rect = surrender_button.get_rect()
    surrender_button_rect.center = (screen_width * .75, board_height + (screen_height - board_height) * .5)

    # Load buttons for horse/elephant swapping and generate rects
    left_button = pygame.transform.scale(pygame.image.load(os.path.join('images', 'left_icon.png')), (int(piece_width * .8), int(piece_width * .8)))
    right_button = pygame.transform.scale(pygame.image.load(os.path.join('images', 'right_icon.png')), (int(piece_width * .8), int(piece_width * .8)))
    both_button = pygame.transform.scale(pygame.image.load(os.path.join('images', 'both_icon.png')), (int(piece_width * .8), int(piece_width * .8)))
    none_button = pygame.transform.scale(pygame.image.load(os.path.join('images', 'none_button.png')), (int(piece_width * .8), int(piece_width * .8)))

    left_button_rect = left_button.get_rect()
    left_button_rect.center = (screen_width * .2, board_height + (screen_height - board_height) * .64)
    right_button_rect = right_button.get_rect()
    right_button_rect.center = (screen_width * .4, board_height + (screen_height - board_height) * .64)
    both_button_rect = both_button.get_rect()
    both_button_rect.center = (screen_width * .6, board_height + (screen_height - board_height) * .64)
    none_button_rect = none_button.get_rect()
    none_button_rect.center = (screen_width * .8, board_height + (screen_height - board_height) * .64)

    # Load button to select yes for AI
    yes_button = pygame.transform.scale(pygame.image.load(os.path.join('images', 'yes_button.png')), (int(piece_width * .8), int(piece_width * .8)))
    yes_button_rect = yes_button.get_rect()
    yes_button_rect.center = (screen_width * .2, board_height + (screen_height - board_height) * .64)

    # Init Janggi game
    game = JanggiGame()

    def update_gui():
        """Update the pygame gui"""
        game_board = game.get_janggi_board().get_board()
        for key_col in sorted(game_board):
            row_counter = 1
            for value in game_board[key_col]:
                if value != "__" and value.get_type() == "Soldier":
                    if value.get_team() == 'red':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(red_soldier, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                    if value.get_team() == 'blue':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(blue_soldier, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                elif value != "__" and value.get_type() == "General":
                    if value.get_team() == 'red':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(red_king, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                    if value.get_team() == 'blue':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(blue_king, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                elif value != "__" and value.get_type() == "Guard":
                    if value.get_team() == 'red':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(red_guard, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                    if value.get_team() == 'blue':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(blue_guard, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                elif value != "__" and value.get_type() == "Horse":
                    if value.get_team() == 'red':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(red_horse, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                    if value.get_team() == 'blue':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(blue_horse, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                elif value != "__" and value.get_type() == "Elephant":
                    if value.get_team() == 'red':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(red_elephant, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                    if value.get_team() == 'blue':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(blue_elephant, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                elif value != "__" and value.get_type() == "Chariot":
                    if value.get_team() == 'red':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(red_chariot, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                    if value.get_team() == 'blue':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(blue_chariot, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                elif value != "__" and value.get_type() == "Cannon":
                    if value.get_team() == 'red':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(red_cannon, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))
                    if value.get_team() == 'blue':
                        coord = (board_to_coord_map[key_col + str(row_counter)][0], board_to_coord_map[key_col + str(row_counter)][1])
                        screen.blit(blue_cannon, (coord[0] - piece_width // 2, coord[1] - piece_height // 2))

                row_counter += 1
        return True

    # Run game loop
    running = True
    from_coords = None
    to_coords = None
    from_rect = None
    blue_swap = False
    red_swap = False
    swap_over = False
    ai_decision = False
    ai_yes = False

    # CODE BELOW IS THE GAME LOOP
    while running:
        skip_flag = False
        surrender_flag = False
        player_turn = game.get_player_turn()

        if red_swap is True and blue_swap is True:
            swap_over = True

        if to_coords is not None:
            from_coords = None
            to_coords = None
            from_rect = None

        for event in pygame.event.get():
            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and from_coords is not None and swap_over is True and ai_decision is True:
                for rectangle in piece_rect_list:
                    if rectangle.collidepoint(event.pos):
                        to_coords = rectangle.center
            if event.type == pygame.MOUSEBUTTONUP and from_coords is None and swap_over is True and ai_decision is True:
                for rectangle in piece_rect_list:
                    if rectangle.collidepoint(event.pos):
                        from_coords = rectangle.center
                        from_rect = rectangle
            if event.type == pygame.MOUSEBUTTONUP and surrender_button_rect.collidepoint(event.pos) and swap_over is True and ai_decision is True:
                surrender_flag = True
            if event.type == pygame.MOUSEBUTTONUP and skip_button_rect.collidepoint(event.pos) and swap_over is True and ai_decision is True:
                skip_flag = True
            if event.type == pygame.MOUSEBUTTONUP and left_button_rect.collidepoint(event.pos) and swap_over is False and ai_decision is True:
                if player_turn == 'blue':
                    blue_swap = True
                    game.swap_horse_elephant(player_turn, 'left')
                    game.change_turn()
                else:
                    red_swap = True
                    game.swap_horse_elephant(player_turn, 'left')
                    game.change_turn()
            if event.type == pygame.MOUSEBUTTONUP and right_button_rect.collidepoint(event.pos) and swap_over is False and ai_decision is True:
                if player_turn == 'blue':
                    blue_swap = True
                    game.swap_horse_elephant(player_turn, 'right')
                    game.change_turn()
                else:
                    red_swap = True
                    game.swap_horse_elephant(player_turn, 'right')
                    game.change_turn()
            if event.type == pygame.MOUSEBUTTONUP and both_button_rect.collidepoint(event.pos) and swap_over is False and ai_decision is True:
                if player_turn == 'blue':
                    blue_swap = True
                    game.swap_horse_elephant(player_turn, 'both')
                    game.change_turn()
                else:
                    red_swap = True
                    game.swap_horse_elephant(player_turn, 'both')
                    game.change_turn()
            if event.type == pygame.MOUSEBUTTONUP and none_button_rect.collidepoint(event.pos) and swap_over is False and ai_decision is True:
                if player_turn == 'blue':
                    blue_swap = True
                    game.swap_horse_elephant(player_turn, 'neither')
                    game.change_turn()
                else:
                    red_swap = True
                    game.swap_horse_elephant(player_turn, 'neither')
                    game.change_turn()
            if event.type == pygame.MOUSEBUTTONUP and yes_button_rect.collidepoint(event.pos) and ai_decision is False:
                ai_decision = True
                ai_yes = True
            if event.type == pygame.MOUSEBUTTONUP and none_button_rect.collidepoint(event.pos) and ai_decision is False:
                ai_decision = True

        # pass turn if skip_flag is true
        player_in_check_at_beginning_of_turn = game.is_in_check(game.get_player_turn())
        if skip_flag is True and player_in_check_at_beginning_of_turn is False:
            game.change_turn()

        # End game if player surrenders
        if surrender_flag is True:
            if player_turn == 'red':
                game.set_game_state('BLUE_WON')
            else:
                game.set_game_state('RED_WON')

        from_location = None
        to_location = None
        # Convert from, to coords to location input
        for key, val in board_to_coord_map.items():
            if from_coords == (int(val[0]), int(val[1])):
                from_location = key
            if to_coords == (int(val[0]), int(val[1])):
                to_location = key

        # Make Move
        if from_location is not None and to_location is not None:
            game.make_move(from_location, to_location)

        # Clear Screen
        screen.fill(white_color)

        # Add background image
        screen.blit(bg_scaled, (0, 0))

        # Add dead space at bottom
        screen.blit(bottom_space, (0, board_height))

        # fill in the bottom space with board color
        pygame.Surface.fill(bottom_space, board_color)

        # get team color and update move prompter
        if player_turn == 'red' and ai_yes is False:
            turn = red_color
        elif player_turn == 'blue':
            turn = blue_color
        else:
            turn = black_color

        # Place colored circle at bottom to signal turn
        if game.get_game_state() == "UNFINISHED" and swap_over is True:
            filled_circle_size = (0.14 * screen_height) // 4
            circle_thickness = int(.2 * filled_circle_size)
            pygame.draw.circle(screen, turn, (screen_width // 2, board_height + (screen_height - board_height) * .5), filled_circle_size)
            pygame.draw.circle(screen, black_color, (screen_width // 2, board_height + (screen_height - board_height) * .5), filled_circle_size + circle_thickness, circle_thickness)

        # add pass and surrender buttons as long as game is unfinished
        if game.get_game_state() == "UNFINISHED" and swap_over is True and (ai_yes is False or (ai_yes is True and player_turn == 'blue')):
            screen.blit(skip_button, skip_button_rect)
            screen.blit(surrender_button, surrender_button_rect)

        # Draw rectangle around selected from move
        if from_rect is not None and swap_over is True and game.get_game_state() == "UNFINISHED":
            from_square = game.get_janggi_board().get_square(from_location)
            if from_square != "__":
                if player_turn == 'red' and from_square.get_team() == 'red':
                    pygame.draw.rect(screen, red_color, from_rect, 4)
                elif player_turn == 'blue' and from_square.get_team() == 'blue':
                    pygame.draw.rect(screen, blue_color, from_rect, 4)

        # print winning message after checkmate
        if game.get_game_state() == 'BLUE_WON':
            winning_message = endgame_font.render("Blue Team Won", False, blue_color)
            screen.blit(winning_message, ((screen_width - winning_message.get_width()) // 2, ((screen_height - board_height) - winning_message.get_height()) // 2 + board_height))
        elif game.get_game_state() == 'RED_WON':
            winning_message = endgame_font.render("Red Team Won", False, red_color)
            screen.blit(winning_message, ((screen_width - winning_message.get_width()) // 2, ((screen_height - board_height) - winning_message.get_height()) // 2 + board_height))

        # output buttons/message for elephant/horse swap at beginning of game
        if swap_over is False and ai_decision is True:
            team_turn = game.get_player_turn()
            swap_prompt_message = team_turn.upper() + " Please choose to swap Horses and Elephants. Choose Left, Both, Right, or None"
            swap_prompt = message_font.render(swap_prompt_message, False, black_color)
            screen.blit(swap_prompt, ((screen_width - swap_prompt.get_width()) // 2, ((screen_height - board_height) - swap_prompt.get_height()) * .1 + board_height))
            screen.blit(left_button, left_button_rect)
            screen.blit(right_button, right_button_rect)
            screen.blit(both_button, both_button_rect)
            screen.blit(none_button, none_button_rect)

        # output AI decision buttons at beginning of game
        if ai_decision is False:
            ai_prompt_message = "Would you like to play vs a computer? Select Yes or No"
            ai_prompt = message_font.render(ai_prompt_message, False, black_color)
            screen.blit(ai_prompt, ((screen_width - ai_prompt.get_width()) // 2, ((screen_height - board_height) - ai_prompt.get_height()) * .1 + board_height))
            screen.blit(none_button, none_button_rect)
            screen.blit(yes_button, yes_button_rect)

        # Update gui
        update_gui()
        pygame.display.update()

        # AI loop
        if ai_yes is True and player_turn == 'red' and swap_over is True and game.get_game_state() == "UNFINISHED":
            # necesary to add loop in case the AI tries to make an invalid move (since the auto_move functions doesn't validate all moves)
            loop_iterations = 0
            while game.get_player_turn() == 'red':
                move_set = game.auto_move(player_turn)
                pygame.time.delay(1000)
                game.make_move(move_set[0], move_set[1])
                player_in_check_at_beginning_of_turn = game.is_in_check(game.get_player_turn())
                # Sometimes the AI gets stuck if their only valid move is to pass, since passing isn't in move set
                if loop_iterations > 10 and player_in_check_at_beginning_of_turn is False:
                    game.change_turn()
                loop_iterations += 1

    pygame.quit()


if __name__ == '__main__':
    main()
