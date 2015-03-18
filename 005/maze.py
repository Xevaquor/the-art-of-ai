# coding=utf-8
__author__ = 'Xev'

Directions = {
    'East': (1, 0),
    'North': (0, -1),
    'South': (0, 1),
    'West': (-1, 0),
    'NorthEast': (1, -1),
    'NorthWest': (-1, -1),
    'SouthEast': (1, 1),
    'SouthWest': (-1, 1)
}


# Typy pól (kafli). Kolejno: puste, ściana, bagno, pole startowe, wyjście
class Tile:
    def __init__(self):
        pass

    Blank, Wall, Swamp, Start, Target = range(5)


# Klasa reprezentująca problem znajdowania drogi w labiryncie.
class Maze:
    def __init__(self):
        # układ pól na planszy
        self.layout = []
        self.expanded = []
        self.shape = (0, 0)
        # miejsce startowe
        self.startState = None
        self.targetState = None
        self.expanded_count = 0
    def get_target_state(self):
        return self.targetState

    def load_from_file(self, filename):
        rows = 0
        with open(filename, 'r') as f:
            for line in f:
                self.layout.append([])
                self.expanded.append([])
                rows += 1
                cols = 0
                for char in line:
                    tile = None
                    if char == ' ':
                        tile = Tile.Blank
                    elif char == 'X':
                        tile = Tile.Wall
                    elif char == '.':
                        tile = Tile.Swamp
                    elif char == 'S':
                        tile = Tile.Start
                        self.startState = (cols, rows - 1)
                    elif char == 'T':
                        tile = Tile.Target
                        self.targetState = (cols, rows - 1)
                    elif char == '\r' or char == '\n':
                        break
                    else:
                        raise Exception('Unknown tile type: \'' + char + '\'')
                    self.layout[-1].append(tile)
                    self.expanded[-1].append(False)
                    cols += 1
        self.shape = (cols, rows)

    # pobierz kafel pod daną pozycją. state jest krotką (x,y)
    def get_tile(self, state):
        x, y = state
        return self.layout[y][x]

    # sprawdź czy podany stan (x,y) jest stanem końcowym
    def is_target_state(self, state):
        return self.get_tile(state) == Tile.Target

    def get_shape(self):
        return self.shape

    # pobierz stan początkowy
    def get_start_state(self):
        return self.startState

    # pobierz stan po podjęciu decyzji d w stanie state
    def get_after_decision(self, state, d):
        x, y = state
        dx, dy = Directions[d]
        return x + dx, y + dy

    # rozwiń wierzchołek
    def get_children(self, state):
        x, y = state
        children = []
        # dla wszystkich potencjalnie możliwych ruchów
        for d in Directions:
            dx, dy = Directions[d]
            # w zależności od typu kafla ustaw koszt przejścia
            t = self.get_tile((x + dx, y + dy))
            cost = 2 if t == Tile.Swamp else 1
            if dx != 0 and dy != 0:
                cost *= 1.41
            # jeżeli kafel nie jest ścianą dodaj do następników
            if t != Tile.Wall:
                children.append(((x + dx, y + dy), d, cost))
        # zapamiętaj fakt rozwinięcia (póki co nieistotne)
        self.expanded[y][x] = True

        return children

    def is_expanded(self, state):
        x, y = state
        self.expanded_count += 1
        return self.expanded[y][x]


m = Maze()
m.load_from_file('simple_maze.txt')
