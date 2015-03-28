# coding=utf-8
from Queue import PriorityQueue
from MazeCoin import *
from numpy import sqrt


class Node:
    def __init__(self):
        self.parent = None
        self.state = None
        self.step = None
        self.cost = 0
        pass


def find_nearest(node_pos, goal):
    if len(goal) == 0:
        return 0
    return min([taxi(node_pos, x) for x in goal])


def heuristics(node, instance):
    node_pos = (node[0], node[1])
    target_pos = (instance.get_target_state()[0], instance.get_target_state()[1])
    return taxi(node_pos, target_pos)


def taxi(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def astar(instance, h=heuristics):
    closed = []  # zbiór zamknięty
    # inicjujemy zbiór otwarty stanem początkowym. Decyzję ustawiamy na null
    # koszt na 0 - nie ma to znaczenia. Rodzicem jest również null (jest to
    # korzeń drzewa
    # fringe dla UCS jest kolejką priorytetową (niższy priorytet powoduje szybsze zdjęcie
    #elementu
    #enqueue - put
    #dequeue - get
    fringe = PriorityQueue()
    #format wierzchołka to:
    #(priorytet,[(stan, decyzja, koszt), rodzic])
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
        #ignorujemy koszt pobrany z kolejki, zamiast niego używamy własności cost węzła
        node = fringe.get()[1]
        node_cost = node.cost

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

            #print node.state, children
            #i dla każdego następnika
            for child in children:
                child_state, child_step, child_cost = child
                #dodaj informację o poprzedniku (node jest rodzicem child)
                #jako koszt ustaw sumę następnika i koszt dojścia do rodzica -
                #został on odczytany przy rozpakowywaniu krotki zwróconej przez
                #fringe.get()
                heuristic_cost = h(child_state, instance) #koszt do wyjścia oszacowany przez heurystykę
                vertex = Node()
                vertex.step = child_step
                vertex.cost = child_cost + node_cost
                vertex.parent = node
                vertex.state = child_state
                new_node = (vertex.cost + heuristic_cost, vertex) #priorytetem jest dotychczasowy
                #koszt + wartość heurystyki.
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
