import random as r
import string
import time as t
import json

games = {}

# Stała kolejność kolorów
PLAYER_COLORS = ['blue', 'red', 'green', 'yellow']

def get_games():
    games_dump = json.dumps(games, default=lambda x: x.__dict__)
    return json.loads(games_dump)

class Lobby():
    def __init__(self, host_id):
        self.host_id = host_id
        self.number_of_players_connected = 0
        self.game_in_progress = False
        self.players_connected = []  # Lista ID graczy
        self.player_colors = {}  # {player_id: color}
        self.player_on_the_move = None
        self.board_status = get_empty_board()
        self.time_created = t.time()
        self.time_since_last_move = 0

    def touch_lobby(func):
        def wrapper(self, *args, **kwargs):
           self.time_since_last_move = 0
           return func(self, *args, **kwargs)
        return wrapper

def get_empty_board():
    return "000"

def generate_lobby_id():
    pool = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    id = "#" + "".join(r.sample(pool, 7))
    return id

def create_lobby(host_id):
    id = generate_lobby_id()
    while id in games:
        id = generate_lobby_id()
    games[id] = Lobby(host_id=host_id)
    add_player_to_lobby(host_id, id)
    return id

def get_lobby_status(lobby_id):
    lobby = games[lobby_id]
    lobby_dump = json.dumps(lobby, default=lambda x: x.__dict__)
    return json.loads(lobby_dump)

def generate_player_id(length=8):
    pool = string.ascii_letters + string.digits
    return ''.join(r.choices(pool, k=length))

def add_player_to_lobby(player_id, lobby_id):
    if lobby_id not in games:
        return -1, f"Lobby {lobby_id} not found"
    lobby = games[lobby_id]

    if lobby.number_of_players_connected > 3:
        return -2, f"Lobby {lobby_id} is full"
    if player_id in lobby.players_connected:
        return -3, f"Player {player_id} is already in the lobby {lobby_id}"

    # Przydziel kolor
    used_colors = set(lobby.player_colors.values())
    available_colors = [c for c in PLAYER_COLORS if c not in used_colors]
    if not available_colors:
        return -4, "No available colors"

    assigned_color = available_colors[0]
    lobby.player_colors[player_id] = assigned_color
    lobby.players_connected.append(player_id)
    lobby.number_of_players_connected += 1

    # Jeśli to pierwszy gracz, on zaczyna
    if lobby.player_on_the_move is None:
        lobby.player_on_the_move = player_id

    return 0, f"Player {player_id} joined as {assigned_color}"
