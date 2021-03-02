# Author: Connor Hollenbach
# Date: 2/22/2021
# A program that implements Classes to play the board game "Janggi" aka Korean chess

###############################################################################################
################# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS ###################
# Initializing the board
"""
The board is initialized as a dict of lists. Each key in the dictionary corresponds to the letter/column of a location,
and key maps to a list of length 10 (the actual squares on the board). Thus location 'b4' would be the 4th value in the
list associated with the key 'b'. The gameboard is initialized as its own class, and an instance of that class is
created when the JanggiGame class gets initialized. The gameboard class, in addition to storing the dict of lists itself
as a data member, also tracks locations that are considered palaces (simply as a list of string locations). In
JanggiGame, GamePiece classes (see next scenario) are hardcoded into their starting positions on the dict of lists.

1. for key in 'a'-'i', generate a list of length 10
2. When JanggiGame is called, GamePiece instances are hardcoded into their starting positions in the above dict of lists
"""
# Determining how to represent pieces at a given location on the board
"""
Pieces are represented by classes. I made a GamePiece parent class, and then created separate child classes for each
type of piece (General, Horse, etc.) that inherit the parent class. The parent class stores the team/type of the piece
and has some basic getter methods, and the child classes have a valid_moves method that returns all possible moves for
a given piece type, given its location and the state of the gameboard. When JanggiGame is initialized, it also places
instances of each piece at the appropriate location on the Gameboard.

1. Create child classes (each unique type of piece) that inherit from the parent GamePiece class
2. Store instances of these classes within the dict of lists that represents the board (e.g. at key ='e' and index = 8, 
which is the 9th square, store instance of General class for the blue team.)
"""
# Determining how to validate a given move according to the rules for each piece, turn taking and other game rules.
"""
Each child class of GamePiece contains a method called valid_moves. This method takes the current gameboard, and the 
location of the gamepiece as parameters. Given that info, every location a gamepiece can move to is generated according 
to its movement rules. For pieces like the general, guard, and soldier, which only move one square, this is fairly
simple, as there are a limited number of squares, so each square is examined to make sure it is on the board, and either
empty or occupied by an enemy. The General and guards are also checked to make sure the location is in the palace. For 
horses and elephants, there are still a limited number of movement squares, but squares along the way are examined to 
insure there are no blocking pieces, since these units can't jump. For the cannon and the chariot, we loop through 
squares in a line to determine where the first blocking piece is for the chariot (either before a friendly piece, or at
an enemy piece, or the edge of the board), or to determine if there is a jumping piece and where the subsequent blocking
piece is for the cannon.

In the make_move method of JanggiGame, validation is performed to insure that the piece being selected belongs to the 
player who's turn it is (player turn is a data member in JanggiGame). There are also checks in that method to make sure
that a player's move does not leave them in check, which would be an illegal move.

1. for each gamepiece child class, have a valid_moves method
2. for each direction the piece can move in (depends on piece/in palace or not), determine if subsequent square/move
is empty, occupied by friendly piece, or occupied by enemy
3. Depending on the gamepiece, either add square to move list, stop going in that direction, or continue onto next
square in that direction (e.g. chariot would stop at the first ally piece, a cannon can jump the first non-cannon ally 
piece, but soldier only needs to check 1 square out)
"""
# Modifying the board state after each move.
"""
There is a method in the GameBoard class called set_square(). This method takes a location and a value (expected to 
either be a gamepiece instance or a string "__" which I use to represent an empty square. The method assigns the value
to the given location in the dict of lists. In my make_move method, after validating the move, I call this method twice.
Once to move the piece to the new location, and once to set the old location as empty.

1. Validate move is legal
2. call set_square on location to move to, setting it's value as the value of the square being moved from
3. call set_square on location being moved from, setting it's value as empty, aka this string "__"
4. If piece being moved is a general update data member in JanggiGame to track the general's location
"""
# Determining how to track which player's turn it is to play right now.
"""
The JanggiGame has a data member called player_turn. This is either 'red' or 'blue'. There is another method called
change_turn that simply flips this from 'red' -> 'blue' (if player_turn == 'red' then player_turn = 'blue' else player_turn = 'red')
or vice versa. In the make_move method, after a move is  validated, the board is updated, and any potential checkmate is
evaluated, the change_turn method is called to change the turn of the player. This data member is used at the beginning
of the make_move method to determine if the piece being moved belongs to the player who's turn it is (pieces have a data
member for which team they belong to).

1. Initialize game with 'blue' as the player turn
2. at the beginning of the make_move method, check that piece being moved belongs to player whos turn it is
3. after each valid move, change the player turn to the other player
"""
# Determining how to detect the checkmate scenario.
"""
This works in two parts. Part 1 is detecting check scenarios. I have a method called get_all_enemy_moves that takes a
team as a parameter. This method loops through the boardm and for all pieces on teh opposing team, adds the pieces moves
to a growing set. Then the is_in_check method simply determines if the teams general location (stored as a data member
in the JanggiGame class) is in the list of all enemy moves. If yes, then team is in check, otherwise team is not in 
check.

Part 2 occurs whenever a player's move puts the enemy into check. When this happens, the is_in_checkmate method is
called. This method will iterate through the board, and for each piece belonging to the player, for each move available
to that piece, make the move, see if the player is still in check, the roll the move back. If at any point the player
is NOT in check, we return False, as they have some move that will end the check, but if we check every piece they have
and no move will break the check, we return True as they are in checkmate.

Written out in pseudocode, this looks like:
1. Get all available spaces enemy can move to
2. Check if own team general in list of enemy move spaces
3. If yes, for every piece on own team, for every move for every piece, make the move
4. Get all available spaces enemy can move to after possible move made
5. Check if own team general in list of enemy move spaces
6. Roll the possible move back
7. If the own team general was still in check, repeat steps 3-6 for all pieces on own team
8. If own team general at any point is not in check anymore after possible move, there is no checkmate
9. If after every piece and every move is evaluated, the general never left, check, there is a checkmate
"""
# Determining which player has won and also figuring out when to check that.
"""
At the end of the make_move method, after the move is made, a the opposing player is examed to determine if they are in
check. If they are, they are evaluated to see if they are in check mate (see above description for more technical 
details on how this is done). If they are in checkmate, the the player who just moved has won, so we can update the 
game status and end the game.

1. make valid move
2. evaluate if enemy in check
3. if yes, evaluate if enemy in checkmate
4. if yes, change game state and end game
"""
###############################################################################################

# Using external package to add color to terminal print in order to see red/blue side better
# Not used for any functionality required in README
# from termcolor import colored


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
        print("Attempting: ", location_a, "->", location_b)
        # get value at location_a and location_b, and location of general
        # the latter two are used to roll the game back if necessary
        from_square = self._janggi_board.get_square(location_a)
        to_square = self._janggi_board.get_square(location_b)
        general_location = self.get_general_loc(self.get_player_turn())

        # Pass turn if location_a and location_b are the same, and the player isn't in check
        player_in_check_at_beginning_of_turn = self.is_in_check(self._player_turn)
        if location_a == location_b and player_in_check_at_beginning_of_turn is False:
            self.change_turn()
            return True
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

            # Insure that player does not end their turn in check
            # If the player does end their turn in check, we need to roll the move back and return False
            # A player ends their turn in check if they move into check (invalid) or do not move out of check if placed
            # into it by the enemy in the previous turn
            # We make the move first so that we can check all enemy moves after player move, as player move can effect
            # enemy move possibilities
            player_in_check_after_move = self.is_in_check(self._player_turn)
            if player_in_check_after_move is True:
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
        # If not importing colored module, use normal print
        return "GN"
        # return colored("GN", self._team)

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
    """
    Guard Clas. Can move 1 space in any direction within the palace.
    """
    def __init__(self, team):
        """Init Guard with new type"""
        super().__init__(team)
        self._type = "Guard"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        # If not importing colored module, use normal print
        return "GD"
        # return colored("GD", self._team)

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
    Horse Class. Can move one step orthogonally and one step diagonally outward. Cannot jump units.
    """
    def __init__(self, team):
        """Init Horse with new type"""
        super().__init__(team)
        self._type = "Horse"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        # If not importing colored module, use normal print
        return "HS"
        # return colored("HS", self._team)

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
        # If not importing colored module, use normal print
        return "EL"
        # return colored("EL", self._team)

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
    """
    Chariot Class. Moves in an orthogonal line, and can move diagonally within palace.
    """
    def __init__(self, team):
        """Init Chariot with new type"""
        super().__init__(team)
        self._type = "Chariot"

    def __str__(self):
        """Override print method to display gamepiece in terminal"""
        # If not importing colored module, use normal print
        return "CH"
        # return colored("CH", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])
        palace_squares = gameboard.get_both_palaces()

        # Chariot moves in 4 orthogonal directions while outside palace, and 8 directions inside palace
        for direction in ['up', 'right', 'down', 'left', 'upright', 'downright', 'downleft', 'upleft']:
            stop_flag = False
            last_col = starting_col
            last_row = starting_row
            # all moves in a line up to edge of board/ally piece/onto enemy piece are valid
            # if in palace, can move diagonally to edge of palace as well
            if direction in ['upright', 'downright', 'downleft', 'upleft'] and location not in gameboard.get_palace(palace_squares):
                # if chariot is not in palace, it can't move diagonally
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
                elif direction in ['upright', 'downright', 'downleft', 'upleft'] and next_location not in palace_squares:
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
        # If not importing colored module, use normal print
        return "CA"
        #return colored("CA", self._team)

    def valid_moves(self, location, gameboard):
        """Determines valid moves for the piece, given the starting location, and the state of the gameboard"""
        move_list = []
        starting_col = location[0]
        starting_row = int(location[1:])
        palace_squares = gameboard.get_both_palaces()

        # Cannon moves in 4 orthogonal directions while outside palace, and 8 directions inside palace. It must jump a unit
        for direction in ['up', 'right', 'down', 'left', 'upright', 'downright', 'downleft', 'upleft']:
            stop_flag = False
            unit_counter = 0
            last_col = starting_col
            last_row = starting_row
            # all moves in a line up to edge of board/ally piece/onto enemy piece are valid
            # if in palace, can move diagonally to edge of palace as well
            if direction in ['upright', 'downright', 'downleft', 'upleft'] and location not in gameboard.get_palace(
                    palace_squares):
                # if cannon is not in palace, it can't move diagonally
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
                elif direction in ['upright', 'downright', 'downleft', 'upleft'] and next_location not in palace_squares:
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
        # If not importing colored module, use normal print
        return "SD"
        # return colored("SD", self._team)

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
        # Check diagonal moves for being in the palace
        for move in [move_diag_1, move_diag_2]:
            if gameboard.get_square(move) is not None and move in palace_squares and (
                        gameboard.get_square(move) == '__' or
                        gameboard.get_square(move).get_team() != self.get_team()):
                move_list.append(move)

        return set(move_list)


def main():
    """Main function to test out code"""
    game = JanggiGame()
    while game.get_game_state() == 'UNFINISHED':
        game.get_janggi_board().display_board()
        turn = game.get_player_turn().upper()
        from_location, to_location = input(turn + " " + "Please make your move: ").split()
        move = game.make_move(from_location, to_location)
        if move is False:
            print("Invalid move, please make a valid move")
    print('\n'*10)
    print(game.get_game_state())


if __name__ == '__main__':
    main()
