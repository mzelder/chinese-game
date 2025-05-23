import string
import random as r


games = []


class Lobby:
    def __init__(self):
        self.id = None


def generate_lobby_id():
    """
    Adds two numbers. (TEST DOCSTRING)

    @param a First number.
    @param b Second number.
    @return Sum of a and b.
    """
    pool = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    id = "#" + "".join(r.sample(pool, 7))
    return id


print(generate_lobby_id())
