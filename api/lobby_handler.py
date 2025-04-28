import random as r
import string
import time as t
import json

games = {} # custom data structure TBD

class Lobby():
    def __init__(self):
        self.number_of_players_connected = 0
        self.game_in_progress = False
        self.players_connected = []
        self.player_on_the_move = None
        self.board_status = get_empty_board()
        self.time_created = t.time()
        self.time_since_last_move = 0

    def touch_lobby(func):
        def wrapper(self, *args, **kwargs):
           self.time_since_last_move = 0
           func(self, *args, **kwargs)
        return wrapper
    

def get_empty_board():
    return "000"


def generate_lobby_id():
    pool = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    id = "#" + "".join(r.sample(pool, 7))
    return id

def create_lobby():
    id = generate_lobby_id()
    while id in games: # reroll the id if a game with that id already exists (highly unlikely)
        id = generate_lobby_id()
    games[id] = Lobby()
    return id


def get_lobby_status(lobby_id):
    lobby = games[lobby_id]
    lobby_dump = json.dumps(lobby, default=lambda x: x.__dict__)
    return json.loads(lobby_dump)