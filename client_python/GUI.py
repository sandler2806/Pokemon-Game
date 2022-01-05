import sys

from pygame import gfxdraw
import pygame
from pygame import *
import copy
from types import SimpleNamespace

import client_python.config as cnf


class GUI:
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    screen = display.set_mode((1080, 720), depth=32, flags=RESIZABLE)
    radius = 15
    FONT: font

    @staticmethod
    def init_GUI():
        # init pygame
        WIDTH, HEIGHT = 1080, 720

        pygame.init()

        GUI.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        pygame.font.init()

        GUI.FONT = pygame.font.SysFont('Arial', 20, bold=True)

        # get data proportions
        GUI.min_x = min(list(cnf.gameMap.nodes.values()), key=lambda n: n.pos[0]).pos[0]
        GUI.min_y = min(list(cnf.gameMap.nodes.values()), key=lambda n: n.pos[1]).pos[1]
        GUI.max_x = max(list(cnf.gameMap.nodes.values()), key=lambda n: n.pos[0]).pos[0]
        GUI.max_y = max(list(cnf.gameMap.nodes.values()), key=lambda n: n.pos[1]).pos[1]

        """
        The code below should be improved significantly:
        The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
        """

    @staticmethod
    def draw():
        screen = GUI.screen
        background_img = pygame.image.load(r'..\data\pok.png')
        background = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))

        buttonW = 50
        buttonH = 30
        buttonX = screen.get_width() / 1.1
        buttonY = screen.get_height() / 15

        counterX = screen.get_width() / 50
        gradeX = screen.get_width() / 50
        gradeY = buttonY - buttonH * 2 / 3
        timerY = gradeY - buttonH * 2 / 3

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if buttonX <= mouse[0] <= buttonX + buttonW and buttonY <= mouse[1] <= screen.get_height() + buttonH:
                    cnf.client.stop_connection()
                    sys.exit()
        # refresh surface
        my_formatter = "{0:.1f}"
        timer = my_formatter.format(cnf.timeToEnd / 1000)
        smallfont = pygame.font.SysFont('Corbel', 17, bold=True)
        pygame.draw.rect(screen, (227, 244, 91), [buttonX, buttonY, buttonW, buttonH])
        screen.blit(smallfont.render('stop', True, (0, 0, 0)), (buttonX + buttonW / 6, buttonY + buttonH / 4))
        screen.blit(smallfont.render('move counter:', True, (0, 0, 0)), (counterX + buttonW / 4, buttonY))
        screen.blit(smallfont.render('grade:', True, (0, 0, 0)), (gradeX + buttonW / 4, gradeY))
        screen.blit(smallfont.render(str(cnf.grade), True, (0, 0, 0)), (gradeX + 5 * buttonW / 4, gradeY))
        screen.blit(smallfont.render(str(cnf.movecounter), True, (0, 0, 0)), (counterX + 10 * buttonW / 4, buttonY))
        screen.blit(smallfont.render('time left:', True, (0, 0, 0)), (gradeX + buttonW / 4, timerY))
        screen.blit(smallfont.render(str(timer), True, (0, 0, 0)), (gradeX + 6.5 * buttonW / 4, timerY))

        # draw nodes
        for n in cnf.gameMap.nodes.values():
            x = GUI.my_scale(n.pos[0], x=True)
            y = GUI.my_scale(n.pos[1], y=True)

            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  GUI.radius, Color(64, 80, 174))
            gfxdraw.aacircle(screen, int(x), int(y),
                             GUI.radius, Color(255, 255, 255))

            # draw the node id
            id_srf = GUI.FONT.render(str(n.id), True, Color(255, 255, 255))
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
                src_x = GUI.my_scale(src.pos[0], x=True)
                src_y = GUI.my_scale(src.pos[1], y=True)
                dest_x = GUI.my_scale(dest.pos[0], x=True)
                dest_y = GUI.my_scale(dest.pos[1], y=True)

                # draw the line
                pygame.draw.line(screen, Color(0, 0, 0),
                                 (src_x, src_y), (dest_x, dest_y))

        # draw agents
        scaledPok = copy.deepcopy(cnf.pokemons)
        for p in scaledPok:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=GUI.my_scale(
                float(x), x=True), y=GUI.my_scale(float(y), y=True))

        scaledAgents = copy.deepcopy(cnf.agents)
        for a in scaledAgents:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=GUI.my_scale(
                float(x), x=True), y=GUI.my_scale(float(y), y=True))

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

    @staticmethod
    def scale(data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values
    @staticmethod
    def my_scale(data, x=False, y=False):
        if x:
            return GUI.scale(data, 50, GUI.screen.get_width() - 50, GUI.min_x, GUI.max_x)
        if y:
            return GUI.scale(data, 50, GUI.screen.get_height() - 50, GUI.min_y, GUI.max_y)
