from pygame import gfxdraw
import pygame
from pygame import *
import copy
from types import SimpleNamespace

import client_python.config as cnf

min_x: float
min_y: float
max_x: float
max_y: float
screen = display.set_mode((1080, 720), depth=32, flags=RESIZABLE)
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
    min_x = min(list(cnf.gameMap.nodes.values()), key=lambda n: n.pos[0]).pos[0]
    min_y = min(list(cnf.gameMap.nodes.values()), key=lambda n: n.pos[1]).pos[1]
    max_x = max(list(cnf.gameMap.nodes.values()), key=lambda n: n.pos[0]).pos[0]
    max_y = max(list(cnf.gameMap.nodes.values()), key=lambda n: n.pos[1]).pos[1]

    """
    The code below should be improved significantly:
    The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
    """


def draw():
    global radius, FONT, screen
    buttonW = 50
    buttonH = 30
    buttonX = screen.get_width() / 10
    buttonY = screen.get_height() / 15

    counterX = screen.get_width() / 1.3
    gradeX = screen.get_width() / 1.3
    gradeY = buttonY + buttonH

    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:

            # if the mouse is clicked on the
            # button the game is terminated
            if buttonX <= mouse[0] <= buttonX + buttonW and buttonY <= mouse[1] <= screen.get_height() + buttonH:
                pygame.quit()
    # refresh surface
    screen.fill(Color(0, 0, 0))

    smallfont = pygame.font.SysFont('Corbel', 17)
    pygame.draw.rect(screen, (255, 255, 255), [buttonX, buttonY, buttonW, buttonH])
    screen.blit(smallfont.render('stop', True, (255, 0, 0)), (buttonX + buttonW / 4, buttonY))
    screen.blit(smallfont.render('move counter:', True, (255, 0, 0)), (counterX + buttonW / 4, buttonY))
    screen.blit(smallfont.render('grade:', True, (255, 0, 0)), (gradeX + buttonW / 4, gradeY))
    screen.blit(smallfont.render(str(cnf.grade), True, (255, 0, 0)), (gradeX + 5*buttonW / 4, gradeY))
    screen.blit(smallfont.render(str(cnf.movecounter), True, (255, 0, 0)), (counterX +10*buttonW / 4, buttonY))

    # (width / 2 + 50, height / 2)
    # draw nodes
    for n in cnf.gameMap.nodes.values():
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
    for src in cnf.gameMap.get_all_v().values():
        for dest in cnf.gameMap.all_out_edges_of_node(src.id).keys():
            # find the edge nodes
            # src = next(n for n in gameMap.nodes.values() if n.id == e.src)
            # dest = next(n for n in graph.Nodes if n.id == e.dest)
            dest = cnf.gameMap.get_node(dest)

            # scaled positions
            src_x = my_scale(src.pos[0], x=True)
            src_y = my_scale(src.pos[1], y=True)
            dest_x = my_scale(dest.pos[0], x=True)
            dest_y = my_scale(dest.pos[1], y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126),
                             (src_x, src_y), (dest_x, dest_y))

    # draw agents
    scaledPok = copy.deepcopy(cnf.pokemons)
    for p in scaledPok:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    scaledAgents = copy.deepcopy(cnf.agents)
    for a in scaledAgents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    for agent in scaledAgents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)

    for p in scaledPok:
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