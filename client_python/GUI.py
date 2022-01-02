from ctypes import Union

from pygame import gfxdraw
import pygame
from pygame import *
from pygame.surface import SurfaceType
from pygame.time import Clock

from client_python.config import *

min_x: float
min_y: float
max_x: float
max_y: float
screen
radius = 15
FONT: font


def init_GUI():
    global min_y, min_x, max_x, max_y, screen, FONT
    # init pygame
    WIDTH, HEIGHT = 1080, 720

    pygame.init()

    screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
    pygame.font.init()

    FONT = pygame.font.SysFont('Arial', 20, bold=True)

    # get data proportions
    min_x = min(list(gameMap.nodes.values()), key=lambda n: n.pos[0]).pos[0]
    min_y = min(list(gameMap.nodes.values()), key=lambda n: n.pos[1]).pos[1]
    max_x = max(list(gameMap.nodes.values()), key=lambda n: n.pos[0]).pos[0]
    max_y = max(list(gameMap.nodes.values()), key=lambda n: n.pos[1]).pos[1]

    """
    The code below should be improved significantly:
    The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
    """


def draw():
    global radius, FONT, screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in gameMap.nodes.values():
        x = my_scale(n.pos[0], x=True)
        y = my_scale(n.pos[1], y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for src in gameMap.get_all_v().keys():
        for dest in gameMap.all_out_edges_of_node(src).keys():
            # find the edge nodes
            # src = next(n for n in gameMap.nodes.values() if n.id == e.src)
            # dest = next(n for n in graph.Nodes if n.id == e.dest)

            # scaled positions
            src_x = my_scale(src.pos[0], x=True)
            src_y = my_scale(src.pos[1], y=True)
            dest_x = my_scale(dest.pos[0], x=True)
            dest_y = my_scale(dest.pos[1], y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126),
                             (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked
    # in the same way).
    for p in pokemons:
        if p.type > 0:
            pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
        else:
            pygame.draw.circle(screen, Color(255, 0, 0), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()



def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)
