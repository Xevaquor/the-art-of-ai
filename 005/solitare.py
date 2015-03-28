from astar import astar
import copy

Moves = {
    'W':(0,-1),
    'S':(1,0),
    'N':(-1,0),
    'E':(0,1)
}

def t2l(t):
    l = []
    for x in range(5):
        i = []
        for y in range(5):
            i.append(t[x][y])
        l.append(i)
    return l

def print_state(s):
    for x in range(5):
        print s[x][0], s[x][1], s[x][2], s[x][3], s[x][4]

guard = 0

def h(node, instance):
    global guard
    guard += 1
    count = 0
    for x in range(5):
        for y in range(5):
            if node[x][y]:
                count += 1
    if guard % 1000 == 0: print count
    return count * 2

def stones_left(board):
    count = 0
    for x in range(5):
        for y in range(5):
            if board[x][y]:
                count += 1
    return count

class solitare:
    def __init__(self):
        self.start_state = [[True, True, True, True, True],
                            [True, True, True, True, True],
                            [True, True, True, True, True],
                            [True, True, False, True, True],
                            [True, True, True, True, True],
                            ]


    def is_target_state(self, s):
        count = 0
        for x in range(5):
            for y in range(5):
                if s[x][y]:
                    count += 1
                if count == 2:
                    return False
        #print count
        return True

    def get_start_state(self):
        return self.start_state

    def is_valid_move(self, move, state):
        x,y,dir = move
        if state[x][y] == False:
            return False

        dx, dy = Moves[dir]
        newx, newy = x + dx, y + dy

        if newx < 0 or newx >= 5 or newy < 0 or newy >= 5:
            return False

        if state[newx][newy] == False:
            return False

        newx += dx
        newy += dy

        if newx < 0 or newx >= 5 or newy < 0 or newy >= 5:
            return False

        return state[newx][newy] == False



    def get_after_move(self, state, move):
        start = stones_left(state)
        x,y,dir = move
        dx, dy = Moves[dir]
        middlex, middley = x + dx, y + dy
        lastx, lasty = middlex + dx, middley + dy

        s2 = copy.deepcopy(state)

        s2[x][y] = False
        s2[middlex][middley] = False
        s2[lastx][lasty] = True

        stop = stones_left(s2)

        assert start - 1 == stop

        return s2

    def get_children(self, parent):
        successors = []

        for x in range(5):
            for y in range(5):
                if parent[x][y]:
                    for m in Moves:
                        d = Moves[m]
                        if not self.is_valid_move((x,y,m), parent): continue
                        child = self.get_after_move(parent,(x,y,m)), (m, x,y), 1
                        successors.append(child)
        #print 'legal moves', len(successors), 'left', h(parent, self)
        return successors


l = solitare()
s = l.get_start_state()
print s
#print_state(s)
c = l.get_children(s)

#print l.get_children(s)

res = astar(l, h)
print res
