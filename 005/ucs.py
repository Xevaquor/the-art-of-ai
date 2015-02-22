# coding=utf-8
from Queue import PriorityQueue
from MazeCoin import *

def ucs(instance):
    closed = set()  # zbiór zamknięty
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
    fringe.put((0, [(instance.get_start_state(), None, 0), None]))
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

        #jeśli jesteśmy w stanie docelowym, ustaw cel i zakończ
        if instance.is_target_state(node[0][0]):
            target = node
            break

        #jeśli węzeł nie był rozwijany
        if node[0][0] not in closed:
            #dodaj go do zbioru zamkniętego (innymi słowy oznacz jako rozwinięty)
            closed.add(node[0][0])
            #rozwiń go
            children = instance.get_children(node[0][0])
            #i dla każdego następnika
            for child in children:
                assert instance.get_tile(child[0]) != Tile.Wall

                #sprawdź koszt następnika
                child_cost = child[2]
                #dodaj informację o poprzedniku (node jest rodzicem child)
                #jako koszt ustaw sumę następnika i koszt dojścia do rodzica -
                #został on odczytany przy rozpakowywaniu krotki zwróconej przez
                #fringe.get()
                vertex = (node_cost + child_cost, [child, node])
                #i wrzuć do kolejki (zbioru otwartego)
                fringe.put(vertex)

    #lista decyzji prowadzących do rozwiązania
    solution = []
    #zaczynamy od węzła z wynikiem
    i = target
    #dopóki ma rodzica (nie jesteśmy w korzeniu)
    while i[1] is not None:
        #dodaj decyzję która nas tutaj doprowadziła
        solution.append(i[0][1])
        #przejdź do rodzica
        i = i[1]
    #podążaliśmy od wyjścia do startu przez co trzeba odwrócić kolejność
    solution.reverse()

    return solution
