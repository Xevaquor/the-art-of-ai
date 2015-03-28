# coding=utf-8
from Queue import PriorityQueue
from MazeCoin import *

class Node:
    def __init__(self):
        self.parent = None
        self.state = None
        self.step = None
        self.cost = 0
        pass


def ucs(instance):
    closed = []  # zbiór zamknięty
    # inicjujemy zbiór otwarty stanem początkowym. Decyzję ustawiamy na null
    #koszt na 0 - nie ma to znaczenia. Rodzicem jest również null (jest to
    #korzeń drzewa
    #fringe dla UCS jest kolejką priorytetową (niższy priorytet powoduje szybsze zdjęcie
    #elementu
    #enqueue - put
    #dequeue - get
    fringe = PriorityQueue()
    #format wierzchołka jest nieco inny teraz to:
    #(priorytet,[((x,y), decyzja, koszt), rodzic])
    #jeżeli przez 'node' oznaczyć strukturę wierzchołka używaną poprzednio (w bfs i dfs)
    #to teraz jest to: (priorytet, node)
    #jest to wymagane przez kolejkę.
    root_node = Node()
    root_node.parent = None
    root_node.cost = 0
    root_node.step = None
    root_node.state = instance.get_start_state()
    fringe.put((0, root_node))
    #znaleziony cel
    target = None

    while True:
        #jeśli zbiór otwarty jest pusty to nie istnieje droga do celu
        if fringe.empty():
            return []
        #pobierz kolejny węzeł z kolejki - ten o najniższym priorytecie
        #zmiena node jest takie samego typu jak poprzednio (pobrany wierzchołek
        #rozpakowaliśmy)
        node_cost, node = fringe.get()

        #print node.state

        #jeśli jesteśmy w stanie docelowym, ustaw cel i zakończ
        if instance.is_target_state(node.state):
            target = node
            break

        #jeśli węzeł nie był rozwijany
        if node.state not in closed:
            #dodaj go do zbioru zamkniętego (innymi słowy oznacz jako rozwinięty)
            closed.append(node.state)
            #rozwiń go
            children = instance.get_children(node.state)


            #i dla każdego następnika
            for child in children:
                child_state, child_step, child_cost = child
                #assert instance.get_tile(child[0]) != Tile.Wall
                #print child_state
                #dodaj informację o poprzedniku (node jest rodzicem child)
                #jako koszt ustaw sumę następnika i koszt dojścia do rodzica -
                #został on odczytany przy rozpakowywaniu krotki zwróconej przez
                #fringe.get()
                vertex = Node()
                vertex.step = child_step
                vertex.cost = child_cost + node_cost
                vertex.parent = node
                vertex.state = child_state
                new_node = (vertex.cost, vertex)
                #i wrzuć do kolejki (zbioru otwartego)
                fringe.put(new_node)

    #lista decyzji prowadzących do rozwiązania
    solution = []
    #zaczynamy od węzła z wynikiem
    i = target
    #dopóki ma rodzica (nie jesteśmy w korzeniu)
    while i.parent is not None:
        #dodaj decyzję która nas tutaj doprowadziła
        solution.append(i.step)
        #przejdź do rodzica
        i = i.parent
    #podążaliśmy od wyjścia do startu przez co trzeba odwrócić kolejność
    solution.reverse()

    return solution
