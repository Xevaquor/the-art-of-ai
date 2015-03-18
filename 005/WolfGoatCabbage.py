# coding=utf-8
__author__ = 'Xev'

from ucs import ucs
from astar import astar

Directions = {
    'East': (1, 0),
    'North': (0, -1),
    'South': (0, 1),
    'West': (-1, 0)}


# Typy pól (kafli). Kolejno: puste, ściana, bagno, pole startowe, wyjście
class Tile:
    def __init__(self):
        pass

    Blank, Wall, Swamp, Start, Target = range(5)


class State:
    def __init__(self):
        self.human = False
        self.wolf = False
        self.goat = False
        self.cabbage = False

    def to_tuple(self):
        return self.human, self.wolf, self.goat, self.cabbage

    def from_tuple(self, t):
        self.human = t[0]
        self.wolf = t[1]
        self.goat = t[2]
        self.cabbage = t[3]

    def __str__(self):
        return 'Human: ' + str(self.human) + ' Wolf: ' + str(self.wolf) + ' Goat: ' + str(
            self.goat) + ' Cabbage: ' + str(self.cabbage)


# Klasa reprezentująca problem znajdowania drogi w labiryncie.
class WolfGoatCabbage:
    def __init__(self):

        # miejsce startowe
        # human, wolf, goat, cabbage
        self.startState = State()
        self.expanded_nodes = 0

        #self.startState.wolf = True
        #self.startState.human = False
        #self.startState.cabbage = True
        #self.startState.goat = False

    # sprawdź czy podany stan (x,y, c) jest stanem końcowym
    def is_target_state(self, state):
        s = State()
        s.from_tuple(state)
        return s.human and s.wolf and s.goat and s.cabbage

    # pobierz stan początkowy
    def get_start_state(self):
        return self.startState.to_tuple()

    # pobierz stan po podjęciu decyzji d w stanie state
    def get_after_decision(self, state, d):
        assert False

    def is_lose_state(self, s):
        return s.wolf == s.goat and s.wolf != s.human or s.goat == s.cabbage and s.goat != s.human

    # rozwiń wierzchołek
    def get_children(self, state):
        self.expanded_nodes += 1
        s = State()
        s.from_tuple(state)
        children = []

        if self.is_lose_state(s):
            return []

        #zawsze można przepłynąć pustą łódką
        no_transport = State()
        no_transport.human = not s.human
        no_transport.wolf = s.wolf
        no_transport.goat = s.goat
        no_transport.cabbage = s.cabbage

        children.append((no_transport.to_tuple(), "MOVE HUMAN", 1))

        if s.human == s.wolf:
            xd = State()
            xd.human = not s.human
            xd.wolf = not s.wolf
            xd.goat = s.goat
            xd.cabbage = s.cabbage
            children.append((xd.to_tuple(), "MOVE WOLF", 1))
        if s.human == s.goat:
            xd = State()
            xd.human = not s.human
            xd.goat = not s.goat
            xd.wolf = s.wolf
            xd.cabbage = s.cabbage
            children.append((xd.to_tuple(), "MOVE GOAT", 1))
        if s.human == s.cabbage:
            xd = State()
            xd.human = not s.human
            xd.cabbage = not s.cabbage
            xd.goat = s.goat
            xd.wolf = s.wolf
            children.append((xd.to_tuple(), "MOVE CABBAGE", 1))

        return children


wgc = WolfGoatCabbage()
'''
dd = wgc.get_start_state()
print dd
c = wgc.get_children(dd)
print c
q = (False, False, True, False)
print wgc.get_children(q)
'''

def h(state, instance):
    s=0
    for x in state:
        if x:
            s+=1
    print s
    return s

#sol = astar(wgc, lambda s, x: len(filter(lambda i: i, s)))
sol = astar(wgc, h)
print wgc.expanded_nodes, sol


