class Board:
    def __init__(self):
        self.board = self.generate_ludo_board()

    def generate_ludo_board(self):
        return {i: 'x' for i in range(1, 53)}  # Plansza 52 pol, 'x' oznacza puste pole

    def update_position(self, pawn, old_position, new_position):
        if old_position in self.board:
            self.board[old_position] = 'x'  # Czyscimy stara pozycje
        self.board[new_position] = pawn.color[0]  # Ustawiamy pionek (np. 'R' dla Red)

board = Board()

class Player:
    allowed_colors = ("Yellow", "Green", "Blue", "Red", None)  # Dozwolone kolory
    start_positions = {  # Przypisane pola startowe do kolorow
        "Red": 1,
        "Blue": 14,
        "Yellow": 28,
        "Green": 42,
        None: None  # Jesli kolor jest None, start rowniez jest None, nwm po co niech jest None
    }

    def __init__(self, color, name):
        if color not in Player.allowed_colors:
            raise ValueError(f'Niepoprawny kolor: {color}')
        self.color = color  # Kolor gracza
        self.pawns = 4  # Kazdy zaczyna z 4 pionkami
        self.start = Player.start_positions[color]  # Pozycja startowa w zaleznosci od koloru
        self.name = name  # Nick gracza

class Pawn:
    def __init__(self, player: Player, board: Board):
        self.color = player.color  # Pobieramy kolor od gracza
        self.position = player.start  # Kazdy pionek zaczyna na swojej pozycji startowej
        self.board = board  # Odwolanie do planszy
        self.board.update_position(self, None, self.position)  # Umieszczamy pionek na planszy

    def move(self, n):
        old_position = self.position
        new_position = (self.position + n - 1) % 52 + 1  # Zapewnia cyklicznosc planszy, czyli jedziemy po okregu
        self.position = new_position

        self.board.update_position(self, old_position, new_position)  # Aktualizacja planszy

        print(f"Pionek {self.color} przesunal sie z {old_position} na {new_position}") #Mozliwe ze zbedne
