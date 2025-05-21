import string
import random as r


games = []

class Lobby:
    def __init__(self):
        self.id = None


def generate_lobby_id():
    pool = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    id = "#" + "".join(r.sample(pool, 7))
    return id

print(generate_lobby_id())