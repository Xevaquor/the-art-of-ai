import pygame
import sys
from pygame.locals import *
import numpy as np
from MazeCoin import MazeCoin, Tile
from bfs import *
from dfs import *
from ucs import *
from astar import astar
from maze import Maze

show_expanded = True

screen_x = 1024
screen_y = 768
frame = 0
maze = MazeCoin()
maze.load_from_file("medium_coin.txt")
n, m = maze.shape
print maze.shape

y_res = screen_y / m
x_res = screen_x / n

square = min(x_res, y_res)
field = np.zeros([n, n])

scale = 1.

run = False
pygame.init()
pygame.time.set_timer(USEREVENT + 1, 200)

path = ucs(maze)
path.reverse()
print maze.expanded_count

wnd = pygame.display.set_mode((screen_x, screen_y), RESIZABLE)
caption = "Maze"
pygame.display.set_caption(caption)

tile_size = 20

tiles_mapping = {
    Tile.Start: (255, 255, 0),
    Tile.Target: (0, 255, 0),
    Tile.Wall: (0, 0, 127),
    Tile.Swamp: (127, 127, 0),
    Tile.Blank: (0, 0, 0)
}
heroPos = maze.get_start_state()
heroHasMoved = True

#run = True


def draw(h, w):
    global wnd
    global heroPos
    wnd = pygame.display.set_mode((h, w), RESIZABLE)

    surf = pygame.Surface((n * tile_size, m * tile_size))

    surf.fill((0, 0, 0))
    for y in range(m):
        for x in range(n):
            x_pos = x * tile_size
            y_pos = y * tile_size
            val = maze.get_tile((x, y, None))
            #val = maze.get_tile((x, y))
            color = tiles_mapping[val]
            pygame.draw.rect(surf, color, (x_pos, y_pos, tile_size, tile_size))
            if show_expanded and maze.is_expanded((x, y)):
                pygame.draw.circle(surf, (255, 0, 0), (x_pos + tile_size / 2, y_pos + tile_size / 2),
                                 tile_size / 8, 0)




    for coin in heroPos[2]:
        xcoin, ycoin = coin
        pygame.draw.circle(surf, (255, 255, 0), (xcoin * tile_size + tile_size / 2,
                                                 ycoin * tile_size + tile_size / 2),
                           tile_size / 2, 0)

    # draw hero
    # print heroPos
    pygame.draw.circle(surf, (255, 255, 255), (heroPos[0] * tile_size + tile_size / 2,
                                               heroPos[1] * tile_size + tile_size / 2),
                       tile_size / 2, 0)

    wnd.fill((0, 0, 0))
    # noinspection PyUnboundLocalVariable
    aspect = 1. * x / y
    # ^ I have completely no idea what is going here, but it seems working
    '''if w < h:
        h = int(w / aspect)
    else:
        w = int(h * aspect)
    '''
    # wnd.blit(pygame.transform.scale(surf, (m * 10, n * 10)), (0, 0))
    wnd.blit(surf, (0, 0))
    global heroHasMoved
    global frame
    if heroHasMoved:
        heroHasMoved = False
        pygame.image.save(surf, "makegif\\" + ("%05d" % frame)+ ".png")
        frame += 1

    pygame.display.flip()


def handle_events(events):
    global run
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Run = True
        elif event.type == VIDEORESIZE:
            draw(event.w, event.h)
            screen_x = event.w
            screen_y = event.h
        elif event.type == USEREVENT + 1:
            if run and len(path) > 0:
                step = path.pop()
                global heroPos
                global heroHasMoved
                heroPos = maze.get_after_decision(heroPos, step)
                heroHasMoved = True
                # print heroPos

        else:
            # print event
            pass


draw(500, 500)
# pygame.draw.rect(wnd, (255,0,0), (50,50,100,100))

while True:
    handle_events(pygame.event.get())
    draw(screen_x, screen_y)
    pygame.display.flip()
    run = True
