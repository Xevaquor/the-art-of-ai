from ucs import ucs


Moves = {
    '01':(0,1),
    '02': (0,2),
    '10':(1,0),
    '12':(1,2),
    '20':(2,0),
    '21':(2,1)
}

class jars:
    def __init__(self):
        self.start_state = (7,0,0)
        self.capacity = (7,4,3)

    def is_target_state(self, s):
        return s[0] == 2 and s[1] == 2 and s[2] == 3

    def get_start_state(self):
        return self.start_state

    def get_after_move(self, state, move):
        source = move[0]
        destination = move[1]

        dst_capacity_left = self.capacity[destination] - state[destination]
        transfer_volume = min(state[source], dst_capacity_left)

        successor = list(state)
        successor[source] -= transfer_volume
        successor[destination] += transfer_volume

        return tuple(successor)

    def get_children(self, parent):
        successors = []
        for m in Moves:
            v = Moves[m]
            child = self.get_after_move(parent, v), m, 1
            successors.append(child)

        return successors


jar = jars()
s = (8,0,0)
dd =  jar.get_after_move(s, (0,1))
print jar.get_children(dd)

print ucs(jar)