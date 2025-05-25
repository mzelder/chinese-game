import random as r
import string
import time as t
import json

games = {}

def get_games():
    """
    Get all current game lobbies.
    @return: Dictionary of all game lobbies serialized to JSON
    """
    games_dump = json.dumps(games, default=lambda x: x.__dict__)
    return json.loads(games_dump)


class Board():
    """
    Class representing the game board state and paths.
    """
    def __init__(self):
        """
        Initialize a new game board with starting positions and paths.
        """
        self.start_tile_R = 43
        self.start_tile_B = 4
        self.start_tile_G = 30
        self.start_tile_Y = 17
        self.max_regular_tiles = 52 # how many regular tiles are there? not counting 'r1', 'r2', 'b1' etc...
        self.board = self.create_empty_board()

    def create_path(self, color):
        """
        Create movement path for a specific player color.
        @param color: The color to create path for ('r' for red, 'g' for green, 'b' for blue, 'y' for yellow)
        @return: List of tile positions in movement order for the specified color
        @raises Exception: If an invalid color is provided
        """
        if color == 'r':
            start_tile = self.start_tile_R
        elif color == 'g':
            start_tile = self.start_tile_G
        elif color == 'b':
            start_tile = self.start_tile_B
        elif color == 'y':
            start_tile = self.start_tile_Y
        else:
            raise (Exception, "Invalid pawn path! Critical error.")

        return \
        [str(n) for n in range(start_tile, self.max_regular_tiles + 1)] + \
        ([str(n) for n in range(1, start_tile - 1)]) + \
        ([f'{color}1', f'{color}2', f'{color}3', f'{color}4', f'{color}5', f'{color}_finish'])

    def create_empty_board(self):
        """
        Initialize and return a new empty game board structure.
        @return: Dictionary containing
        """
        board = {}
    
        board['paths'] = {}
        board['paths']['red'] = self.create_path('r')
        board['paths']['blue'] = self.create_path('b')
        board['paths']['green'] = self.create_path('g')
        board['paths']['yellow'] = self.create_path('y')

        board['positions'] = {}
        board['positions']['red'] = {1:None, 2:None, 3:None, 4:None}
        board['positions']['green'] = {1:None, 2:None, 3:None, 4:None}
        board['positions']['blue'] = {1:None, 2:None, 3:None, 4:None}
        board['positions']['yellow'] = {1:None, 2:None, 3:None, 4:None}


        return board

     
class Lobby():
    """
    Class representing a game lobby with players and game state.
    """
    def __init__(self, host_id):
        self.host_id = host_id
        self.number_of_players_connected = 0
        self.game_in_progress = False
        self.players_connected = []
        self.player_on_the_move = None
        self.board_status = Board()
        self.time_created = t.time()
        self.time_since_last_move = 0
        self.who_won = None


    def touch_lobby(func):
        """
        Initialize a new game lobby.
        @param host_id: ID of the player who created the lobby
        """
        def wrapper(self, *args, **kwargs):
           self.time_since_last_move = 0
           func(self, *args, **kwargs)
        return wrapper
    


def generate_lobby_id():
    """
    Generate a random lobby ID.
    @return: String lobby ID starting with #
    """
    pool = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    id = "#" + "".join(r.sample(pool, 7))
    return id

def create_lobby(host_id):
    """
    Create a new game lobby.
    @param host_id: ID of the player creating the lobby
    @return: ID of the newly created lobby
    """
    id = generate_lobby_id()
    while id in games: # reroll the id if a game with that id already exists (highly unlikely)
        id = generate_lobby_id()
    games[id] = Lobby(host_id=host_id)
    add_player_to_lobby(host_id, id)
    games[id].player_on_the_move = games[id].players_connected[0]
    return id


def get_lobby_status(lobby_id):
    """
    Get status information for a specific lobby.
    @param lobby_id: ID of the lobby to query
    @return: Dictionary of lobby status information
    """
    lobby = games[lobby_id]
    lobby_dump = json.dumps(lobby, default=lambda x: x.__dict__)
    return json.loads(lobby_dump)

def generate_player_id(length=8):
    """
    Generate a random player ID.
    @param length: Length of the ID to generate (default 8)
    @return: String player ID
    """
    pool = string.ascii_letters + string.digits
    return ''.join(r.choices(pool, k=length))

def add_player_to_lobby(player_id, lobby_id):
    """
    Add a player to a lobby.
    @param player_id: ID of the player to add
    @param lobby_id: ID of the lobby to join
    @return: Tuple of (status code, message) indicating success or failure
    """

    if lobby_id not in games:
        return -1, f"Lobby {lobby_id} not found"
    if games[lobby_id].number_of_players_connected > 3:
        return -2, f"Lobby {lobby_id} is full"
    if player_id in games[lobby_id].players_connected:
        return -3, f"Player {player_id} is already in the lobby {lobby_id}"
    games[lobby_id].players_connected.append(player_id)
    games[lobby_id].number_of_players_connected += 1

def move_pawn(lobby_id, color, pawn_idx, target_destination):
    """
    Move a pawn on the game board and advance turn.
    @param lobby_id: ID of the lobby where the move occurs
    @param color: Color of the pawn to move
    @param pawn_idx: Index of the pawn to move (1-4)
    @param target_destination: Destination position for the pawn
    """
    lobby = games[lobby_id]
    lobby.board_status.board['positions'][color][pawn_idx] = target_destination
    idx_of_player_on_the_move = lobby.players_connected.index(lobby.player_on_the_move)
    lobby.player_on_the_move = lobby.players_connected[(idx_of_player_on_the_move + 1) % lobby.number_of_players_connected]

def skip_turn(lobby_id): #not clean but atm i couldnt care less
    """
    Skip the current player's turn.
    @param lobby_id: ID of the lobby where the turn is being skipped
    """
    lobby = games[lobby_id]
    idx_of_player_on_the_move = lobby.players_connected.index(lobby.player_on_the_move)
    lobby.player_on_the_move = lobby.players_connected[(idx_of_player_on_the_move + 1) % lobby.number_of_players_connected]