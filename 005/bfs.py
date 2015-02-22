# coding=utf-8
from Queue import Queue

def bfs(instance):
    closed = set()  # zbiór zamknięty
    #inicjujemy zbiór otwarty stanem początkowym. Decyzję ustawiamy na null
    #koszt na 0 - nie ma to znaczenia. Rodzicem jest również null (jest to
    #korzeń drzewa
    #fringe dla BFS jest kolejką
    #enqueue - put
    #dequeue - get
    fringe = Queue()
    fringe.put([(instance.get_start_state(), None, 0), None])
    #znaleziony cel
    target = None

    while True:
        #jeśli zbiór otwarty jest pusty to nie istnieje droga do celu
        if fringe.empty():
            return []
        #pobierz kolejny węzeł z wierchu stosu
        node = fringe.get()

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
                #dodaj informację o poprzedniku (node jest rodzicem child)
                vertex = [child, node]
                #i wrzuć na szczyt stosu (zbioru otwartego)
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
