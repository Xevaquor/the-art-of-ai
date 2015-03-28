from ucs import ucs


Moves = {
    '0':0,
    '1':1,
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8
}

class lucas:
    def __init__(self):
        self.start_state = (False, False, False, False, None,  True, True, True, True)
        self.target_state = (True, True, True, True, None, False, False, False, False )

    def is_target_state(self, s):
        return s == self.target_state

    def get_start_state(self):
        return self.start_state

    def is_valid_move(self, move, state):
        block_to_move = state[move]
        if block_to_move is None: return False

        if block_to_move == True:
            if move == 0: return False
            if state[move - 1] is None: return True
            if move == 1: return False
            return state[move - 2] is None and state[move - 1] == False

        if block_to_move == False:
            if move == 8: return False
            if state[move + 1] is None: return True
            if move == 7: return False
            return state[move + 2] is None and state[move + 1] == True


    def get_after_move(self, state, move):
        player = state[move]
        destination = None

        if player:
            if state[move-1] is None: destination = move-1
            else : destination = move - 2
        else:
            if state[move+1] is None: destination = move+1
            else : destination = move + 2


        successor = list(state)
        successor[move] = None
        successor[destination] = player

        return tuple(successor)

    def get_children(self, parent):
        successors = []
        for m in Moves:
            v = Moves[m]
            if not self.is_valid_move(v, parent): continue
            child = self.get_after_move(parent, v), m, 1
            successors.append(child)

        return successors


l = lucas()
s = l.get_start_state()
print l.get_children(s)

print ucs(l)
