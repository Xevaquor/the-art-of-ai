from astar import astar
import copy
from ucs import ucs

Moves = {
    'W':(0,-1),
    'S':(1,0),
    'N':(-1,0),
    'E':(0,1)
}

def print_state(s):
    for x in range(5):
        print s[x][0], s[x][1], s[x][2], s[x][3], s[x][4]

guard = 0

def h(node, instance):
    blocks = []
    xs = []
    ys = []
    for y in range(5):
        for x in range(4):
            if node[y][x] == None:
                xs.append(x)
                ys.append(y)
    return 100 - 10* sum(ys)


def stones_left(board):
    count = 0
    for x in range(5):
        for y in range(5):
            if board[x][y]:
                count += 1
    return count

def left_corner( b, state):
        blocks = []
        xs = []
        ys = []
        for y in range(5):
            for x in range(4):
                if state[y][x] == b:
                    xs.append(x)
                    ys.append(y)
        return (min(ys), min(xs))

class block:
    def __init__(self):
        self.start_state = [[1, 0, 0, 2],
                            [1, 0, 0, 2],
                            [3, 4, 5, 6],
                            [7, 7,8, 8],
                            [9, None, None, 10],
                            ]


    def is_target_state(self, s):
        return s[4][1] == 0 and s[4][2] == 0

    def get_start_state(self):
        return self.start_state

    def is_valid_move(self, move, state):
        nr,dr = move

        dy, dx = Moves[dr]
        blocks = []
        for y in range(5):
            for x in range(4):
                if state[y][x] == nr:
                    blocks.append((y,x))

        try:
            for y, x in blocks:
                if state[y+dy][x+dx] is not None:
                    return False
        except:
            return False
        return True


    def get_after_move(self, state, move):
        nr,dr = move

        dy, dx = Moves[dr]
        blocks = []
        for y in range(5):
            for x in range(4):
                if state[y][x] == nr:
                    blocks.append((y,x))

        s2 = copy.deepcopy(state)

        for y,x in blocks:
            #print y, x
            s2[y +dy][x+dx] = nr
            s2[y][x] = None

        return s2





    def get_children(self, parent):
        successors = []
        #print left_corner(0, parent)

        for b in range(11):
            for m in Moves:
                d = Moves[m]
                if not self.is_valid_move((b,m), parent): continue
                child = self.get_after_move(parent,(b,m)), (m, left_corner(b, parent)), 1
                successors.append(child)
        #print 'legal moves', len(successors), 'left', h(parent, self)
        return successors


l = block()
s = l.get_start_state()
print s
#print_state(s)
c = l.get_children(s)

#print l.get_children(s)

res = astar(l,h)
print res
